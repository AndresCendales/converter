## Local Development
```shell
# Run app
 docker-compose -f local.yml up --build           
```
Env variables:



## Deploy production
```shell
 docker-compose -f produccion.yml up --build           
```
Env variables
- MAILGUN_PASSWORD=XXXXXX :Access token of mailgun to send emails.


## Test production
```shell
 docker-compose -f produccion.yml -f production.test.yml up --build           
```
Env Variables
- APP_MODE=TEST: Avoid email notifications
- LIMIT_PROCESSING_TEST=1 : Number in seconds for a task processing. Used for test propouses
