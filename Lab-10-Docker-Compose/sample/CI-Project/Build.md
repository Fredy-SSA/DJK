# Build web and db container

##fredysa can be changed to your DockerHub

```
 cd ~\docker-compose\database\
 docker image build -t fredysa/db:1.0 .

 cd ~\docker-compose\web
docker image build -t fredysa/web:1.0 .

docker image ls

```
## You need to have **docker-compose** installed on your system. 

This is automatically the case if you have installed Docker for Desktop or Docker Toolbox on your Windows or macOS computer. 

Otherwise, you can find detailed installation instructions here: https://docs.docker.com/compose/install/