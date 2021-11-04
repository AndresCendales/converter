## Local Development
```shell
# Run app
 docker-compose -f local.yml up --build           
```
Env variables:



## Deploy production

```shell
# Webserver
 docker-compose -f produccion-webserver.yml up --build           

# Worker
 docker-compose -f produccion-worker.yml up --build           

```

## Test production
The testing environment avoid the use of slack notifications.
```shell
 docker-compose -f produccion.yml -f production.test.yml up --build           
```
Env Variables
- APP_MODE=TEST: Avoid slack notifications
- LIMIT_PROCESSING_TEST=1 : Number in seconds for a task processing. Used for test propouses
