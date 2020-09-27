# **Data Volumes and Configuration**
In the last chapter, we learned how to build and share our own container images. Particular focus was placed on how to build images that are as small as possible by only containing artifacts that are really needed by the containerized application.

In this chapter, we are going to learn how we can work with stateful containers—that is, containers that consume and produce data. We will also learn how to configure our containers at runtime and at image build time, using environment variables and config files.

Here is a list of the topics we're going to discuss:

- [Creating and mounting data volumes](Creating-and-mounting-data-volumes.md)
- [Sharing data between containers](Sharing-data-between-containers.md)
- [Using host volumes](Using-host-volumes.md)
- [Defining volumes in images](Volume.md)
- [Configuring containers](Configuring-containers.md)

# Technical requirements
For this chapter, you need either Docker Toolbox installed on your machine or access to a Linux virtual machine (VM) running Docker on your laptop or in the cloud. Furthermore, it is advantageous to have Docker for Desktop installed on your machine. 

Code are in ~\Lab-03..\sample.

# Summary
In this chapter, we have introduced Docker volumes that can be used to persist states produced by containers and make them durable. We can also use volumes to provide containers with data originating from various sources. We have learned how to create, mount, and use volumes. We have learned various techniques of defining volumes such as by name, by mounting a host directory, or by defining volumes in a container image.

In this chapter, we have also discussed how we can configure environment variables that can be used by applications running inside a container. We have shown how to define those variables in the **docker container run** command, either explicitly, one by one, or as a collection in a configuration file. We have also shown how to parametrize the build process of container images by using build arguments.

In the next chapter, we are going to introduce techniques commonly used to allow a developer to evolve, modify, debug, and test their code while running in a container. 

Further reading
The following articles provide more in-depth information:

- Use volumes, at http://dockr.ly/2EUjTml
- Manage data in Docker, at http://dockr.ly/2EhBpzD
- Docker volumes on Play with Docker (PWD), at http://bit.ly/2sjIfDj
- nsenter —Linux man page, at https://bit.ly/2MEPG0n
- Set environment variables, at https://dockr.ly/2HxMCjS
- Understanding how ARG and FROM interact, at https://dockr.ly/2OrhZgx
