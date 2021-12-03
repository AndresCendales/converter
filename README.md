<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Converter </h3>

  <p align="center">
    An awesome audio files converter
    <br />
    <a href="https://documenter.getpostman.com/view/17477086/UV5aeF2o"><strong>Explore the docs »</strong></a>
    <br />
    <br />
  </p>
</div>

### About the project

Converter is a simple audio converter. It converts audio files to mp3, ogg, wav,  wma.

### Local Development
For local development run the follow command that will start the containers of webserver
worker, broker and posgtres database.

```shell
# Run app
 docker-compose -f local.yml up --build           
```
There is no need to setup  any env variable, because there are declared in the docker-compose file.


### Deploy production

#### AWS Deployment
The deploy is running in aws in different ec2 machines.
All the code related with the system is in the repository, but each machine runs differents containers:
```shell
# Webserver
cd /usr/src/app/ folder #  Move to the path were the files are allocated
docker-compose -f production-webserver.yml up --build # Start the webserver container
```

```shell
# Worker
cd /usr/src/app/ #  Move to the path were the files are allocated
docker-compose -f prod-sqs-worker.yml up --build # Start the worker, broker container
```

#### Heroku Deployment
Run the script named deploy-heroku.sh in the root of the project.
```shell
chmod +x ./deploy-heroku.sh
./deploy-heroku.sh
```



## Test production
For load testing we disable the slack notifications, please run the following command into the web server: 
```shell
cd /usr/src/app/ #  Move to the path were the files are allocated
docker-compose -f prod-sqs-worker.yml up -f production-webserver.test.yml -d --build # Start the webserver         
```
The production-webserver.test.yml set the env variables into test mode app.