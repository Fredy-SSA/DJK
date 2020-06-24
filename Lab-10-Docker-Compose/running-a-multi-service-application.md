# **Running a multi-service application**

In most cases, applications do not consist of only one monolithic block, but rather of several application services that work together. When using Docker containers, each application service runs in its own container. When we want to run such a multi-service application, we can, of course, start all the participating containers with the well-known **docker container run** command, and we have done this in previous chapters. But this is inefficient at best. With the Docker Compose tool, we are given a way to define the application in a declarative way in a file that uses the YAML format.


Let's have a look at the content of a simple **docker-compose.yml** file:

```
version: "2.4"
services:
 web:
    image: fredysa/web:1.0
    build: web
    ports:
    - 80:3000
 db:
    image: fredysa/db:1.0
    build: database
    volumes:
    - pets-data:/var/lib/postgresql/data

volumes:
 pets-data:
```

The lines in the file are explained as follows:

- **version**: In this line, we specify the version of the Docker Compose format we want to use. At the time of writing, this is version 2.4.
- **services**: In this section, we specify the services that make up our application in the services block. In our sample, we have two application services and we call them web and **db**:
**web**: The web service is using an image called **fredysa/web:2.0**, which, if not already in the image cache, is built from the Dockerfile found in the web folder . The service is also publishing container **port 3000** to the host port **80**.
- **db**: The db service, on the other hand, is using the image name **fredysa/db:1.0**, which is a customized **PostgreSQL database**. Once again, if the image is not already in the cache, it is built from the Dockerfile found in the **db** folder . We are mounting a volume called **pets-data** into the container of the db service.
- **volumes**: The volumes used by any of the services have to be declared in this section. In our sample, this is the last section of the file. The first time the application is run, a volume called **pets-data** will be created by Docker and then, in subsequent runs, if the volume is still there, it will be reused. This could be important when the application, for some reason, crashes and has to be restarted. Then, the previous data is still around and ready to be used by the restarted database service.

Note that we are using **version 2.x** of the Docker Compose file syntax. This is the one targeted toward deployments on a single **Docker host**. There exists also a **version 3.x** of the Docker Compose file syntax. This version is used when you want to define an application that is targeted either at **Docker Swarm or Kubernetes**. We will discuss this in more detail starting with, Orchestrators.

# Building images with Docker Compose
Navigate to the ch11 subfolder of the fods folder and then build the images:

```
~\Lab-10-Docker-Compose\sample\docker-compose
docker-compose build

docker-compose -f docker-compose-default.yml up -d
```

If we enter the preceding command, then the tool will assume that there must be a file in the current directory called docker-compose.yml and it will use that one to run. In our case, this is indeed the case and the tool will build the images.

In your Terminal window, you should see an output similar to this:

![ams](./img/l10_ams.png)


Building the Docker image for the web service

In the preceding screenshot, you can see that **docker-compose**first downloads the base image **node:12.12-alpine**, for the web image we're building from Docker Hub. Subsequently, it uses the **Dockerfile** found in the **web** folder to build the image and names it **fredysa/web:2.0**. But this is only the first part; the second part of the output should look similar to this:

![ams](./img/l10_ams1.png)

Building the Docker image for the db service
Here, once again, **docker-compose** pulls the base image, **postgres:12.0-alpine**, from Docker Hub and then uses the Dockerfile found in the **db** folder to build the image we call **fredysa/db:1.0**.

# Running an application with Docker Compose

Once we have built our images, we can start the application using Docker Compose:
```
$ docker-compose up
```
The output will show us the application starting. We should see the following:

```
docker-compose up
Creating network "docker-compose_default" with the default driver
Creating volume "docker-compose_pets-data" with default driver
Creating docker-compose_db_1  ... done
Creating docker-compose_web_1 ... done
Attaching to docker-compose_db_1, docker-compose_web_1
db_1   | The files belonging to this database system will be owned by user "postgres".
db_1   | This user must also own the server process.
db_1   |
db_1   | The database cluster will be initialized with locale "en_US.utf8".
db_1   | The default database encoding has accordingly been set to "UTF8".
db_1   | The default text search configuration will be set to "english".
db_1   |
db_1   | Data page checksums are disabled.
db_1   |
db_1   | fixing permissions on existing directory /var/lib/postgresql/data ... ok
db_1   | creating subdirectories ... ok
db_1   | selecting dynamic shared memory implementation ... posix
db_1   | selecting default max_connections ... 100
db_1   | selecting default shared_buffers ... 128MB
db_1   | selecting default time zone ... UTC
db_1   | creating configuration files ... ok
db_1   | running bootstrap script ... ok
web_1  | Listening at 0.0.0.0:3000
db_1   | performing post-bootstrap initialization ... sh: locale: not found
db_1   | 2020-06-20 05:47:07.634 UTC [29] WARNING:  no usable system locales were found
db_1   | ok
db_1   | syncing data to disk ... ok
db_1   |
```
Running the sample application, part 1
In this first part of the output, we see how Docker Compose does the following:

- Creates a bridge network called **docker-compose_default**
- Creates a volume called **docker-compose_pets-data**
- Creates the two services, **docker-compose_web_1** and **docker-compose_db_1**, and attaches them to the network

Docker Compose then also shows log output generated by the database (blue) and by the web service (yellow) that are both stating up. The third last line in the output shows us that the web service is ready and listens at port **3000**. Remember though that this is the container port and not the host port. We have mapped container port **3000** to host port **80**, and that is the port we will be accessing later on.

Now let's look at the second part of the output:

```
db_1   | Success. You can now start the database server using:
db_1   |
db_1   |     pg_ctl -D /var/lib/postgresql/data -l logfile start
db_1   |
db_1   | initdb: warning: enabling "trust" authentication for local connections
db_1   | You can change this by editing pg_hba.conf or using the option -A, or
db_1   | --auth-local and --auth-host, the next time you run initdb.
db_1   | waiting for server to start....2020-06-20 05:47:09.421 UTC [34] LOG:  starting PostgreSQL 12.3 on x86_64-pc-linux-musl, compiled by gcc (Alpine 9.2.0) 9.2.0, 64-bit
db_1   | 2020-06-20 05:47:09.513 UTC [34] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
db_1   | 2020-06-20 05:47:09.907 UTC [35] LOG:  database system was shut down at 2020-06-20 05:47:08 UTC
db_1   | 2020-06-20 05:47:09.993 UTC [34] LOG:  database system is ready to accept connections
db_1   |  done
db_1   | server started
db_1   | CREATE DATABASE
db_1   |
db_1   |
db_1   | /usr/local/bin/docker-entrypoint.sh: running /docker-entrypoint-initdb.d/init-db.sql
db_1   | CREATE TABLE
db_1   | ALTER TABLE
db_1   | ALTER ROLE
db_1   | INSERT 0 1
db_1   | INSERT 0 1
db_1   | INSERT 0 1
db_1   | INSERT 0 1
db_1   | INSERT 0 1
db_1   | INSERT 0 1
db_1   | INSERT 0 1
db_1   | INSERT 0 1
db_1   | INSERT 0 1
db_1   | INSERT 0 1
db_1   | INSERT 0 1
db_1   | INSERT 0 1
db_1   |
db_1   |
db_1   | waiting for server to shut down....2020-06-20 05:47:12.587 UTC [34] LOG:  received fast shutdown request
db_1   | 2020-06-20 05:47:12.680 UTC [34] LOG:  aborting any active transactions
db_1   | 2020-06-20 05:47:12.682 UTC [34] LOG:  background worker "logical replication launcher" (PID 41) exited with exit code 1
db_1   | 2020-06-20 05:47:12.683 UTC [36] LOG:  shutting down
db_1   | 2020-06-20 05:47:13.442 UTC [34] LOG:  database system is shut down
db_1   |  done
db_1   | server stopped
db_1   |
db_1   | PostgreSQL init process complete; ready for start up.
db_1   |
db_1   | 2020-06-20 05:47:13.613 UTC [1] LOG:  starting PostgreSQL 12.3 on x86_64-pc-linux-musl, compiled by gcc (Alpine 9.2.0) 9.2.0, 64-bit
db_1   | 2020-06-20 05:47:13.614 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
db_1   | 2020-06-20 05:47:13.614 UTC [1] LOG:  listening on IPv6 address "::", port 5432
db_1   | 2020-06-20 05:47:13.805 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
db_1   | 2020-06-20 05:47:14.224 UTC [47] LOG:  database system was shut down at 2020-06-20 05:47:13 UTC
db_1   | 2020-06-20 05:47:14.328 UTC [1] LOG:  database system is ready to accept connections
```

Running the sample application, part 2

We have shortened the second part of the output a bit. It shows us how the database finalizes its initialization. We can specifically see how our initialization script, **init-db.sql**, is applied, which defines a database and seeds it with some data.

We can now open a browser tab and navigate to **http://localhost:3000/pet**. We should be greeted by a wild animal whose picture I took at the Masai Mara national park in Kenya:

![ams](./img/l10_ams4.png)

The sample application in the browser

Refresh the browser a few times to see other cat images. The application selects the current image randomly from a set of 12 images whose URLs are stored in the database.

As the application is running in interactive mode and, thus, the Terminal where we ran Docker Compose is blocked, we can cancel the application by pressing Ctrl + C. If we do so, we will see the following:

```
Gracefully stopping... (press Ctrl+C again to force)
Stopping docker-compose_web_1 ... done
Stopping docker-compose_db_1  ... done
```

We will notice that the database and the web services stop immediately. Sometimes, though, some services will take about 10 seconds to do so. The reason for this is that the database and the web service listen to, and react to, the **SIGTERM**signal sent by Docker while other services might not, and so Docker kills them after a predefined timeout interval of 10 seconds.

If we run the application again with **docker-compose up**, the output will be much shorter:

```
docker-compose up
Starting docker-compose_web_1 ... done
Starting docker-compose_db_1  ... done
Attaching to docker-compose_web_1, docker-compose_db_1
db_1   |
db_1   | PostgreSQL Database directory appears to contain a database; Skipping initialization
db_1   |
db_1   | 2020-06-20 05:50:45.994 UTC [1] LOG:  starting PostgreSQL 12.3 on x86_64-pc-linux-musl, compiled by gcc (Alpine 9.2.0) 9.2.0, 64-bit
db_1   | 2020-06-20 05:50:45.994 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
db_1   | 2020-06-20 05:50:45.994 UTC [1] LOG:  listening on IPv6 address "::", port 5432
web_1  | Listening at 0.0.0.0:3000
db_1   | 2020-06-20 05:50:46.235 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
db_1   | 2020-06-20 05:50:46.572 UTC [21] LOG:  database system was shut down at 2020-06-20 05:49:54 UTC
db_1   | 2020-06-20 05:50:46.715 UTC [1] LOG:  database system is ready to accept connections
```
Output of docker-compose up

This time, we didn't have to download the images and the database didn't have to initialize from scratch, but it was just reusing the data that was already present in the **pets-data**volume from the previous run.

We can also run the application in the background. All containers will run **as daemons**. For this, we just need to use the **-d** parameter, as shown in the following code:

```
$ docker-compose up -d
Starting docker-compose_web_1 ... done
Starting docker-compose_db_1  ... done
```

Docker Compose offers us many more commands than just up. We can use the tool to list all services that are part of the application:
```
 docker-compose ps
```
```
        Name                      Command               State            Ports
---------------------------------------------------------------------------------------
docker-compose_db_1    docker-entrypoint.sh postgres    Up      5432/tcp
docker-compose_web_1   docker-entrypoint.sh /bin/ ...   Up      0.0.0.0:32774->3000/tcp
```

Output of docker-compose ps

This command is similar to **docker container ls**, with the only difference being that **docker-compose** only lists containers or services that are part of the application.

To stop and clean up the application, we use the **docker-compose down** command:

```
 docker-compose down
```
```
Stopping docker-compose_db_1  ... done
Stopping docker-compose_web_1 ... done
Removing docker-compose_db_1  ... done
Removing docker-compose_web_1 ... done
Removing network docker-compose_default
```

If we also want to remove the volume for the database, then we can use the following command:

```
docker volume rm docker-compose_pets-data
```

Alternatively, instead of using the two commands, **docker-compose down** and **docker volume rm <volume name>**, we can combine them into a single command:

```
$ docker-compose down -v
```
```
Stopping docker-compose_web_1 ... done
Stopping docker-compose_db_1  ... done
Removing docker-compose_web_1 ... done
Removing docker-compose_db_1  ... done
Removing network docker-compose_default
Removing volume docker-compose_pets-data
```

Here, the argument **-v**(or **--volumes**) removes named volumes declared in the **volumes** section of the **compose** file and anonymous volumes attached to containers.

Why is there a **docker-compose** prefix in the name of the volume? In the **docker-compose.yml** file, we have called the volume to use **pets-data**. But, as we have already mentioned, Docker Compose prefixes all names with the name of the parent folder of the **docker-compose.yml** file plus an underscore. In this case, the parent folder is called **docker-compose**. If you don't like this approach, you can define a project name explicitly, for example, as follows:

```
$ docker-compose -p my-app up -d
```
which uses a project name my-app for the application to run under.



## Clean up

```
docker-compose -p my-app down -v
```
