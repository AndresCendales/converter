#docker-compose -f prod-webserver.yml up --build -d
#docker tag proyecto-grupo4-202120_app registry.heroku.com/converter-web-server/web

echo "-------------------------------"
echo "STARTING DEPLOYMENT"

echo "-------------------------------"
echo "Web Server deployment started..."
docker build -t registry.heroku.com/converter-web-server/web -f config/Dockerfile .
docker push registry.heroku.com/converter-web-server/web
heroku container:release web --app=converter-web-server
echo "Web Server deployment finished."

echo "-------------------------------"
echo "Worker deployment started..."
docker build -t registry.heroku.com/converter-worker/worker -f worker_sqs/Dockerfile .
docker push registry.heroku.com/converter-worker/worker
heroku container:release worker --app=converter-worker
echo "Worker deployment finished."