# Celery
from celery import Celery

# Database
import psycopg2
from psycopg2 import Error

# Email
import smtplib

# Utils
import os
from datetime import datetime
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
        Notifier().send_notification_to_download(
            original_file_path=original_filename,
            new_format=new_format,
            new_file_path=new_filename
        )


def execute_conversion(user_id, original_filename, new_filename):
    """
    Execute_conversion pass command line to the system wich execute the file conversion
    :param user_id: user_id to save the files in that folder
    :param original_filename
    :param new_filename:
    :return:
    """
    os.system(f"ffmpeg -i files/{user_id}/{original_filename} files/{user_id}/{new_filename} -y")
    logger.info('CeleryTasks', 'execute_conversion',
                f'ruta: files/{user_id}/{original_filename} files/{user_id}/{new_filename}')


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

        query = f"SELECT timestamp FROM tasks WHERE original_file_path = '{original_filename}' AND user_id = {user_id}"
        cursor.execute(query)
        difference = datetime.now() - cursor.fetchone()[0]
        if difference.total_seconds() > 600:
            logger.info("ProccesOutOfTime", 'ProccesOutOfTime', f"El proceso de conversion tardo: {difference.total_seconds()} s")

        logger.info('CeleryTasks', 'update_database_status', f'Estatus actualizado correctamente. El proceso tardo: {difference.total_seconds()} s')

        # Close resources
        cursor.close()
        connection.close()
    except (Exception, Error) as error: \
            logger.error('CeleryTasks', 'error', f'No se puede actualizar el estatus: {error}')


def delete(user_id, filename_to_delete):
    """
    delete a file
    """
    os.system(f"rm files/{user_id}/{filename_to_delete}")


sender = "Coverter <notifier@converter.com>"
receivers = ['Anderson Santamaria <andersonsantamaria3@gmail.com>']


class Notifier:
    def send_notification_to_download(self, original_file_path, new_format, new_file_path):
        self.get_email(original_file_path, new_format, new_file_path)
        self.send_notification(self.email, os.getenv("MAILGUN_PASSWORD"))
        return "email sent.", 200

    def get_email(self, original_file_path, new_format, new_file_path):
        subject = "Converted document!"

        own_message = """Hi! <br/> <br/> 
        The document that you uploaded in the route <b>%s</b>, to be converted to one of a kind <b>%s</b> 
        it's ready, you can find it with on the route <b>%s</b>
        <br/> <br/>
        Best regards from Converter.
        """ % (original_file_path, new_format, new_file_path)

        self.email = """From: %s 
        To: %s 
        MIME-Version: 1.0 
        Content-type: text/html 
        Subject: %s 
        %s
        """ % (sender, receivers, subject, own_message)

    def send_notification(self, email, smtp_password):
        try:
            s = smtplib.SMTP(host='smtp.mailgun.org', port=587)
            s.starttls()
            s.login("postmaster@sandbox5a390ccc8a52448fa5a7f8c6d603e025.mailgun.org", smtp_password)
            s.sendmail(sender, receivers, email)
            logger.info('CeleryTasks', 'send_email', 'Email enviado correctamente')
        except Exception as e:
            logger.error("EmailFailed", 'email_not_sended', f"error: {e}")
