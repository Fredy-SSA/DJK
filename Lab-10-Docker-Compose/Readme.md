# **Docker Compose**

This chapter introduces the concept of an application consisting of multiple services, each running in a container, and how Docker Compose allows us to easily build, run, and scale such an application using a declarative approach.

## This chapter covers the following topics:

- [Demystifying declarative versus imperative](demystifying-declarative-versus-imperative.md)
- [Running a multi-service application](running-a-multi-service-application.md)
- [Building and pushing an application](building-and-pushing-an-application.md)
- [Scaling a service](Scaling-a-service.md)
- [Using Docker Compose overrides](Using-Docker-Compose-overrides.md)


# Technical requirements
The code accompanying this chapter can be found at https://github.com/fredy-ssa/DJK
```
# Download code
git pull https://github.com/Fredy-SSA/jenkins-pipeline.git

cd c:\DJK\Lab-10-Docker-Compose\sample\docker-compose
```

You need to have docker-compose installed on your system. This is automatically the case if you have installed Docker for Desktop or Docker Toolbox on your Windows or macOS computer. Otherwise, you can find detailed installation instructions here: https://docs.docker.com/compose/install/

# Summary
In this chapter, we introduced the **docker-compose tool**. This tool is mostly used to run and scale multi-service applications on a single Docker host. Typically, developers and CI servers work with single hosts and those two are the main users of Docker Compose. The tool is using YAML files as input that contain the description of the application in a declarative way.


# Further reading
The following links provide additional information on the topics discussed in this chapter:

- The official YAML website: http://www.yaml.org/
- Docker Compose documentation: http://dockr.ly/1FL2VQ6
- Compose file version 2 reference: http://dohttps://docs.docker.com/compose/compose-file/compose-file-v2/
- Share Compose configurations between files and projects: https://docs.docker.com/compose/extends/
- How https works:  https://howhttps.works/the-keys/
