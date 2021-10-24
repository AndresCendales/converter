## Local Development
```shell
# Run app
 docker-compose -f local.yml up --build           
```

## Deploy production
```shell
 docker-compose -f produccion.yml up --build           
```

## Test production
```shell
 docker-compose -f produccion.yml -f production.test.yml up --build           
```
