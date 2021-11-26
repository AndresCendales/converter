FROM python:3.8.3-slim

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && apt install ffmpeg -y \
    && pip install psycopg2

COPY ./celery/ /queue
COPY ./util /queue/util
WORKDIR /queue

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

RUN pip install -U setuptools pip
RUN pip install -r requirements.txt
