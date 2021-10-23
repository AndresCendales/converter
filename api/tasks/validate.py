# config
from config import ALLOWED_EXTENSIONS


def allowed_file(filename):
    """ allowed_file return True if the filename is an allowed value"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
