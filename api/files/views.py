# Flask
from flask.views import MethodView
from flask import send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity

# Models
from api.auth.models import User
from api.tasks.models import Task

# Utils
import os

from util import s3_service


class FilesView(MethodView):
    @jwt_required()
    def get(self, filename):
        """
        Get method of file view
        Retrieve a file by the filename
        :return:
        """
        user = User.query.filter_by(username=get_jwt_identity()).first()

        task = Task.query.filter_by(new_file_path=filename, user_id=user.id).first()
        if task is None:
            return {"mensaje": "Aun no esta listo el archivo"}

        #path = os.path.join(os.getenv("UPLOAD_FOLDER"), f"{user.id}/")
        os.system(f"mkdir -p files/{user.id}")
        s3_path = "files/"+str(user.id)+"/"+task.original_file_path
        path = s3_service.s3_download_file(s3_path, str(user.id)+"/"+filename)
        return send_from_directory(path, filename)
