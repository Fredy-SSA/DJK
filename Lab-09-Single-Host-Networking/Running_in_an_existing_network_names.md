# **Running in an existing network names**


The network namespace of the container corresponds to the sandbox of the container network model we described earlier on. As we attach the container to a network, we define an endpoint that connects the container network namespace with the actual network. This way, we have one container per network namespace.

Docker provides an additional way for us to define the network namespace that a container runs in. When creating a new container, we can specify that it should be attached to (or maybe we should say included) in the network namespace of an existing container. With this technique, we can run multiple containers in a single network namespace:

![SHN](./img/l9_shn-11.png)

Multiple containers running in a single network namespace

#  Running in a existing network name

In the preceding diagram, we can see that in the leftmost Network Namespace, we have two containers. The two containers, since they share the same namespace, can communicate on localhost with each other. The network namespace (and not the individual containers) is then attached to **Network 1.**

This is useful when we want to debug the network of an existing container without running additional processes inside that container. We can just attach a special utility container to the network namespace of the container to inspect. This feature is also used by Kubernetes when it creates a pod. We will learn more about Kubernetes and pods in, Introduction to Kubernetes. 

Now, let's demonstrate how this works:

1. First, we create a new bridge network

```
$ docker network create --driver bridge test-net
```

2. Next, we run a container attached to this network:

```
docker container run --name web -it --rm -d --network test-net  alpine:latest /bin/sh
 
```

3. Finally, we run another container and attach it to the network of our web container:

```

docker container run --name containerweb2  -it --rm --network test-net  alpine:latest /bin/sh
```


4. Ping Test

```
ping  web
```

Note that we have shortened the output for readability. Please also note that there is an important difference between running two containers attached to the same network and two containers running in the same network namespace. In both cases, the containers can freely communicate with each other, but in the latter case, the communication happens over localhost.

5. To clean up the container and network, we can use the following command:

```
$ docker container rm --force web
$ docker network rm test-net
```

In the next section, we are going to learn how to expose container ports on the container host.





