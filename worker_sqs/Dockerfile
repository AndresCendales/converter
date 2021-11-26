FROM python:3.8.3-slim

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && apt install ffmpeg -y \
    && pip install psycopg2

COPY ./worker_sqs/ /queue
COPY ./worker_celery/tasks.py ./queue/worker_celery/
COPY ./worker_celery/requirements.txt ./queue
COPY ./util /queue/util
WORKDIR /queue

ENV C_FORCE_ROOT true

RUN pip install -U setuptools pip
RUN pip install -r requirements.txt

CMD [ "python", "./receive_messages.py"]
