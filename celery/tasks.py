# Celery
from celery import Celery

# Utils
import os
import logging

celery = Celery(
    'tasks',
    broker=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
    backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')
)


@celery.task(name='tasks.convert')
def convert(filename, new_format):
    logging.info("conversion in progress...", extra={"file_name": filename, "new_format": new_format})
