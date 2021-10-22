import os

ALLOWED_EXTENSIONS = {'mp3', 'acc', 'ogg', 'wav', 'wma'}

class Config:
    """Set Flask configuration vars."""

    # General Config
    DEBUG = True

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI',
                                             'postgresql+psycopg2://app_usr:app_pwd@127.0.0.1:5432/app_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
