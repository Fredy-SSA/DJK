# Defining liveness and readiness

Container orchestration systems such as Kubernetes and Docker swarm make it significantly easier to deploy, run, and update highly distributed, mission-critical applications. The orchestration engine automates many of the cumbersome tasks such as scaling up or down, asserting that the desired state is maintained at all times, and more.

But, the orchestration engine cannot just do everything automagically. Sometimes, we developers need to support the engine with some information that only we can know about. So, what do I mean by that?

Let's look at a single application service. Let's assume it is a microservice and let's call it service A. If we run **service A** containerized on a Kubernetes cluster, then Kubernetes can make sure that we have the five instances that we require in the service definition running at all times. If one instance crashes, Kubernetes can quickly launch a new instance and thus maintain the desired state. But, what if an instance of the service does not crash, but is unhealthy or just not ready yet to serve requests? It is evident that Kubernetes should know about both situations. But it can't, since healthy or not from an application service perspective is outside of the knowledge of the orchestration engine. Only we application developers can know when our service is healthy and when it is not.

The application service could, for example, be running, but its internal state could have been corrupted due to some bug, it could be in an endless loop, or in a deadlock situation. Similarly, only we application developers know if our service is ready to work, or if it is still initializing. Although it is highly recommended to keep the initialization phase of a microservice as short as possible, it often cannot be avoided if there is a significant time span needed by a particular service so that it's ready to operate. Being in this state of initialization is not the same thing as being unhealthy, though. The initialization phase is an expected part of the life cycle of a microservice or any other application service.

Thus, Kubernetes should not try to kill our microservice if it is in the initialization phase. If our microservice is unhealthy, though, Kubernetes should kill it as quickly as possible and replace it with a fresh instance.

Kubernetes has a concept of probes to provide the seam between the orchestration engine and the application developer. Kubernetes uses these probes to find out more about the inner state of the application service at hand. Probes are executed locally, inside each container. There is a probe for the health – also called liveness – of the service, a startup probe, and a probe for the readiness of the service. Let's look at them in turn.

# Kubernetes liveness probe

Kubernetes uses the liveness probe to decide when a container needs to be killed and when another instance should be launched instead. Since Kubernetes operates at a pod level, the respective pod is killed if at least one of its containers reports as being unhealthy. Alternatively, we can say it the other way around: only if all the containers of a pod report to be healthy, is the pod considered to be healthy.

We can define the liveness probe in the specification for a pod as follows:

```
apiVersion: v1
kind: Pod
metadata:
 ...
spec:
 containers:
 - name: liveness-demo
 image: postgres:12.10
 ...
 livenessProbe:
   exec:
    command: nc localhost 5432 || exit -1
   initialDelaySeconds: 10
   periodSeconds: 5
```

The relevant part is in the **livenessProbe** section. First, we define a command that Kubernetes will execute as a probe inside the container. In our case, we have a PostresSQL container and use the **netcat** Linux tool to probe port **5432** over TCP. The **nc localhost 5432** command is successful once Postgres listens at it.

The other two settings, **initialDelaySeconds** and **periodSeconds**, define how long Kubernetes should wait after starting the container until it first executes the probe and how frequently the probe should be executed thereafter. In our case, Kubernetes waits for 10 seconds prior to executing the first probe and then executes a probe every 5 seconds.

It is also possible to probe an HTTP endpoint instead of using a command. Let's assume we're running a microservice from an image, **acme.com/my-api:1.0**, with an API that has an endpoint called **/api/health** that returns status **200 (OK)** if the microservice is healthy, and **50x (Error)** if it is unhealthy. Here, we can define the liveness probe as follows:

```
apiVersion: v1
kind: Pod
metadata:
  ...
spec:
  containers:
  - name: liveness
    image: acme.com/my-api:1.0
    ...
    livenessProbe:
      httpGet:
        path: /api/health
        port: 3000
      initialDelaySeconds: 5
      periodSeconds: 3
```

In the preceding snippet, I have defined the liveness probe so that it uses the HTTP protocol and executed a **GET** request to the **/api/health** endpoint on port **5000** of localhost. Remember, the probe is executed inside the container, which means I can use localhost.

We can also directly use the TCP protocol to probe a port on the container. But wait a second – didn't we just do that in our first sample, where we used the generic liveness probe based on an arbitrary command? Yes, you're right, we did. But we had to rely on the presence of the **netcat** tool in the container to do so. We cannot assume that this tool is always there. Thus, it is favorable to rely on Kubernetes to do the TCP-based probing for us out of the box. The modified pod spec looks like this:


```
apiVersion: v1
kind: Pod
metadata:
 ...
spec:
 containers:
 - name: liveness-demo
   image: postgres:12.10
   ...
   livenessProbe:
     tcpSocket:
       port: 5432
     initialDelaySeconds: 10
     periodSeconds: 5
```

This looks very similar. The only change is that the type of probe has been changed from **exec** to **tcpSocket** and that, instead of providing a command, we provide the **port** to probe.

Let's try this out:

Navigate to the **~/Lab-13-.../sample/probes** folder and build the Docker image with the following command:

```
docker-compose build
-or
docker image build -t fredysa/demo:1.0 .

docker push fredysa/demo:1.0

docker image ls 

```

Use kubectl to deploy the sample pod that's defined in probes-demo.
yaml:

```
$ kubectl apply -f probes-demo.yaml
```

Describe the pod and specifically analyze the log part of the output:

```
$ kubectl describe pods/probes-demo
```

During the first half minute or so, you should get the following output:

```
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  35s   default-scheduler  Successfully assigned default/probes-demo to minikube
  Normal  Pulled     34s   kubelet, minikube  Container image "fredysa/demo:1.0" already present on machine
  Normal  Created    34s   kubelet, minikube  Created container probes-demo
  Normal  Started    34s   kubelet, minikube  Started container probes-demo

```

Log output of the healthy pod
Wait at least 30 seconds and then describe the pod again. This time, you should see the following output:

```
Events:
  Type     Reason     Age                From               Message
  ----     ------     ----               ----               -------
  Normal   Scheduled  68s                default-scheduler  Successfully assigned default/probes-demo to minikube
  Normal   Pulled     67s                kubelet, minikube  Container image "fredysa/demo:1.0" already present on machine
  Normal   Created    67s                kubelet, minikube  Created container probes-demo
  Normal   Started    67s                kubelet, minikube  Started container probes-demo
  Warning  Unhealthy  24s (x3 over 34s)  kubelet, minikube  Liveness probe failed: cat: /app/healthy: No such file or directory
  Normal   Killing    24s                kubelet, minikube  Container probes-demo failed liveness probe, will be restarted
```

Log output of the pod after it has changed its state to **Unhealthy**
The last two lines are indicating the failure of the probe and the fact that the pod is going to be restarted.

```
Events:
  Type     Reason     Age                  From               Message
  ----     ------     ----                 ----               -------
  Normal   Scheduled  2m32s                default-scheduler  Successfully assigned default/probes-demo to minikube
  Normal   Pulling    2m32s                kubelet, minikube  Pulling image "fredysa/demo:1.0"
  Normal   Pulled     2m23s                kubelet, minikube  Successfully pulled image "fredysa/demo:1.0"
  Normal   Created    71s (x2 over 2m22s)  kubelet, minikube  Created container probes-demo
  Normal   Started    71s (x2 over 2m22s)  kubelet, minikube  Started container probes-demo
  Normal   Pulled     71s                  kubelet, minikube  Container image "fredysa/demo:1.0" already present on machine
  Warning  Unhealthy  26s (x6 over 111s)   kubelet, minikube  Liveness probe failed: cat: /app/healthy: No such file or directory
  Normal   Killing    26s (x2 over 101s)   kubelet, minikube  Container probes-demo failed liveness probe, will be restarted
```



If you get the list of pods, you will see that the pod has been restarted a number of times:

```
$ kubectl get pods
NAME         READY   STATUS    RESTARTS   AGE
probes-demo  1/1     Running   5          7m22s
```

When you're done with the sample, delete the pod with the following command:

```
$ kubectl delete pods/probes-demo
```
Next, we will have a look at the Kubernetes readiness probe.

# Kubernetes readiness probe
Kubernetes uses a readiness probe to decide when a service instance, that is, a container, is ready to accept traffic. Now, we all know that Kubernetes deploys and runs pods and not containers, so it only makes sense to talk about the readiness of a pod. Only if all containers in a pod report to be ready is the pod considered to be ready itself. If a pod reports not to be ready, then Kubernetes removes it from the service load balancers.

Readiness probes are defined exactly the same way as liveness probes: just switch the **livenessProbe** key in the pod spec to **readinessProbe**. Here is an example using our prior pod spec:

```
 ...
spec:
 containers:
 - name: liveness-demo
   image: postgres:12.10
   ...
   livenessProbe:
     tcpSocket:
       port: 5432
     failureThreshold: 2
     periodSeconds: 5
   
   readinessProbe:
     tcpSocket:
       port: 5432
     initialDelaySeconds: 10
     periodSeconds: 5
```

Note that, in this example, we don't really need an initial delay for the liveness probe anymore since we now have a readiness probe. Thus, I have replaced the initial delay entry for the liveness probe with an entry called **failureThreshold**, which is indicating how many times Kubernetes should repeat probing in case of a failure until it assumes that the container is unhealthy.

# Kubernetes startup probe
It is often helpful for Kubernetes to know when a service instance has started. If we define a startup probe for a container, then Kubernetes does not execute the liveness or readiness probes, as long as the container's startup probe does not succeed. Once again, Kubernetes looks at pods and starts executing liveness and readiness probes on its containers if the startup probes of all the pod's containers succeed.

When would we use a startup probe, given the fact that we already have the liveness and readiness probes? There might be situations where we have to account for exceptionally long startup and initialization times, such as when containerizing a legacy application. We could technically configure the readiness or the liveness probes to account for this fact, but that would defeat the purpose of these probes. The latter probes are meant to provide quick feedback to Kubernetes on the health and availability of the container. If we configure for long initial delays or periods, then this would counter the desired outcome.

Unsurprisingly, the startup probe is defined exactly the same way as the readiness and liveness probes. Here is an example:

```
spec:
  containers:
    ..
    startupProbe:
      tcpSocket:
        port: 3000
      failureThreshold: 30
      periodSeconds: 5
  ...
```

Make sure that you define the **failureThreshold * periodSeconds** product so that it's big enough to account for the worst startup time.

**NOTE:** In our example, the max startup time should not exceed 150 seconds.