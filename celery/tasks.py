# Celery
from celery import Celery

# Database
import psycopg2
from psycopg2 import Error

# Utils
import os
from util.logger import Logger

logger = Logger()

celery = Celery(
    'tasks',
    broker=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
    backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')
)


@celery.task(name='tasks.convert')
def convert(user_id, original_filename, new_format, filename_to_delete=""):
    """
    convert orchestra the conversion of file to new format
    :param user_id: user_id of user which request the conversion
    :param original_filename: original string filename with original format
    :param new_format: new format to convert the file
    :param filename_to_delete: filename which will be deleted if exists
    :return:
    """
    new_filename = original_filename.rsplit('.', 1)[0] + "." + new_format

    execute_conversion(user_id, original_filename, new_filename)
    update_database_status(user_id, original_filename, new_filename)

    if filename_to_delete != "":
        delete(user_id, filename_to_delete)

    if os.getenv('APP_MODE') != "TEST":
        send_email()


def execute_conversion(user_id, original_filename, new_filename):
    """
    Execute_conversion pass command line to the system wich execute the file conversion
    :param user_id: user_id to save the files in that folder
    :param original_filename
    :param new_filename:
    :return:
    """
    os.system(f"ffmpeg -i files/{user_id}/{original_filename} files/{user_id}/{new_filename} -y")
    logger.info('CeleryTasks', 'execute_conversion', f'ruta: files/{user_id}/{original_filename} files/{user_id}/{new_filename}')


def update_database_status(user_id, original_filename, new_filename):
    """
    update_database_status change the status to processed for the given filename
    :param original_filename
    :param new_filename:
    :return:
    """
    try:
        # Connect to an existing database
        connection = psycopg2.connect(dsn=os.getenv("DSN", "postgresql://app_usr:app_pwd@127.0.0.1:5432/app_db"))

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        # Executing a SQL query
        query = f"UPDATE tasks SET status = 'processed', new_file_path = '{new_filename}' WHERE original_file_path = '{original_filename}' AND user_id = {user_id};"
        cursor.execute(query)
        connection.commit()

        logger.info('CeleryTasks', 'update_database_status', 'Estatus actualizado correctamente')

        # Close resources
        cursor.close()
        connection.close()
    except (Exception, Error) as error: \
            logger.info('CeleryTasks', 'error', f'No se puede actualizar el estatus: {error}')


def delete(user_name, filename_to_delete):
    """
    delete a file
    """
    os.system(f"rm files/{user_name}/{filename_to_delete}")


def send_email():
    logger.info('CeleryTasks', 'send_email', 'Email enviado correctamente')
    # ToDo
    pass
