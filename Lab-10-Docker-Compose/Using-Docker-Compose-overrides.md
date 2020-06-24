# **Using Docker Compose overrides**

Sometimes, we want to run our applications in different environments that need specific configuration settings. Docker Compose provides a handy capability to address exactly this issue.

Let's make a specific sample. We can define a base Docker Compose file and then define environment-specific overrides. Let's assume we have a file called **docker-compose.base.yml** with the following content:

Navigate to : 
```
cd c:\DJK\Lab-10-Docker-Compose\sample\ci-project\
```
```
version: "2.4"
services:
  web:
    image: fredysa/web:1.0
  db:
    image: fredysa/db:1.0
    volumes:
      - pets-data:/var/lib/postgresql/data

volumes:
  pets-data:
```

This only defines the part that should be the same in all environments. All specific settings have been taken out.

Let's assume for a moment that we want to run our sample application on a CI system, but there we want to use different settings for the database. The Dockerfile we used to create the database image looked like this:

```
FROM postgres:12.0-alpine
COPY init-db.sql /docker-entrypoint-initdb.d/
ENV POSTGRES_USER dockeruser
ENV POSTGRES_PASSWORD dockerpass
ENV POSTGRES_DB pets
```

Notice the three environment variables we define on lines 3 through 5. The Dockerfile of the web service has similar definitions. Let's say that on the CI system, we want to do the following:

**Build the images from code**

Define POSTGRES_PASSWORD as ci-pass
Map container port 3000 of the web service to host port 5000
Then, the corresponding override file would look like this:

```
version: "2.4"
services:
  web:
    build: web
    ports:
      - 5000:3000
    environment:
      POSTGRES_PASSWORD: cipass
  db:
    build: db
    environment:
      POSTGRES_PASSWORD: cipass
```
And we can run this application with the following command:

```
$ docker-compose -f docker-compose.yml -f docker-compose-ci.yml up -d --build
```
Note that with the first -f parameter, we provide the base Docker Compose file, and with the second one, we provide the override. The 
**--build** parameter is used to force docker-compose to rebuild the images.

**Note:** When using environment variables, note the following precedence:
- Declaring them in the Docker file defines a default value
- Declaring the same variable in the Docker Compose file overrides the value from the Dockerfile

Had we followed the standard naming convention and called the base file just **docker-compose.yml** and the override file **docker-compose.override.yml** instead, then we could have started the application with **docker-compose up -d** without explicitly naming the compose files.