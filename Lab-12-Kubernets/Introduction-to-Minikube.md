# Introduction to MiniKube

Minikube is a tool that creates a single-node Kubernetes cluster in VirtualBox or Hyper-V (other hypervisors are supported too) ready to be used during the development of a containerized application.

As stated there, Minikube is a single-node Kubernetes cluster and thus the node is, at the same time, a Kubernetes master as well as a worker node.


# Installing Minikube

If you cannot use Docker for Desktop or, for some reason, you only have access to an older version of the tool that does not yet support Kubernetes, then it is a good idea to install Minikube. Minikube provisions a single-node Kubernetes cluster on your workstation and is accessible through kubectl, which is the command-line tool used to work with Kubernetes.

# Installing Minikube on macOS and Windows
To install Minikube for macOS or Windows, navigate to the following link: https://kubernetes.io/docs/tasks/tools/install-minikube/.

Follow the instructions carefully. If you have Docker Toolbox installed, then you already have a hypervisor on your system since the Docker Toolbox installer also installed VirtualBox. Otherwise, I recommend that you install VirtualBox first.

If you have Docker for macOS or Windows installed, then you already have kubectl installed with it, so you can skip that step too. Otherwise, follow the instructions on the site.

**Note:** Hyper-V can run on three versions of Windows 10: Windows 10 Enterprise, Windows 10 Professional, and Windows 10 Education.
- Install Minikube using Chocolatey
The easiest way to install Minikube on Windows is using Chocolatey (run as an administrator):
```
choco install minikube -y
```
After Minikube has finished installing, close the current CLI session and restart. Minikube should have been added to your path automatically.

- Install Minikube using an installer executable
To install Minikube manually on Windows using Windows Installer, download minikube-installer.exe and execute the installer.

- Install Minikube via direct download
To install Minikube manually on Windows, download minikube-windows-amd64, rename it to minikube.exe, and add it to your path.



# Testing Minikube and kubectl

Once Minikube is successfully installed on your workstation, open a Terminal and test the installation. First, we need to start Minikube. Enter minikube start at the command line. This command may take a few minutes or so to complete. The output should look similar to the following:



Let's make sure that Minikube is running with the following command:

```
 minikube start
```
Once Minikube is ready, we can access its single node cluster using kubectl. We should see something similar to the following:
```
kubectl get nodes
```
![m12](./img/m12-k4.png)

- **Note**, your output may look slightly different. In my case, I am running Minikube on a Windows 10 Pro computer. On a Mac notifications are quite different, but this doesn't matter here.
Now, enter kubectl version and hit Enter to see something like the following screenshot:
```
kubectl version
```
![m12](./img/m12-k5.png)

## Determining the version of the Kubernetes client and server
If the preceding command fails, for example, by timing out, then it could be that your kubectl is not configured for the right context. kubectl can be used to work with many different Kubernetes clusters. Each cluster is called a context. To find out which context kubectl is currently configured for, use the following command:

```
$ kubectl config current-context
```
minikube
The answer should be minikube, as shown in the preceding output. If this is not the case, use kubectl config get-contexts to list all contexts that are defined on your system and then set the current context to minikube, as follows:

```
$ kubectl config use-context minikube
```
The configuration for kubectl, where it stores the contexts, is normally found in **~/.kube/config**, but this can be overridden by defining an environment variable called KUBECONFIG. You might need to unset this variable if it is set on your computer.

For more in-depth information about how to configure and use Kubernetes contexts, consult the link at **https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/**.

Assuming Minikube and kubectl work as expected, we can now use kubectl to get information about the Kubernetes cluster. Enter the following command:

```
$ kubectl get nodes
NAME STATUS ROLES AGE VERSION
minikube Ready master 47d v1.17.3
```


Evidently, we have a cluster of one node, which in my case has Kubernetes v1.17.3 installed on it.


# Open Gui Dashboard Minikube 
```
minikube dashboard
```