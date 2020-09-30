# Docker Compose

## Project Structure:

```
~\DJK\Lab-10-Docker-Compose\Docker-Secrets\docker-compose

```

- docker-compose.yml contents:

```
version: "3.6"

services:

  my_service:
    image: centos:7
    entrypoint: "cat /run/secrets/my_secret"
    secrets:
      - my_secret

secrets:
  my_secret:
    file: ./secret.txt
```
- secret.txt contents:

Whatever you want to write for a secret really.

-  Run this command from the project's root to see that the container does have access to your secret, 
(Docker must be running and docker-compose installed):

```
docker-compose up --build my_service
```
You should see your container output your secret.

 .

