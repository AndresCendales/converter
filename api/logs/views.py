# Views
from flask.views import MethodView
from flask import request
# Utils
from util import s3_service
import os


class LogsView(MethodView):
    """
    LogsView have the methods to handle all logs managment
    """

    @staticmethod
    def get_logs_path(files_path: str) -> str:
        """
        return the logs path
        """
        path_list = files_path.split('/')
        del path_list[-1]
        return '/'.join(path_list) + '/logs'

    def post(self):
        """
        Post method of tasks view
        Upload logs to s3
        :return:
        """
        data = request.json
        local_path = self.get_logs_path(files_path=os.getenv("UPLOAD_FOLDER"))
        filenames = ["CeleryTasks.log", "ProccesViewer.log","ProccesOutOfTime.log", "Datetimes.log"]

        for filename in filenames:
            try:
                s3_path = s3_service.s3_upload_file(
                    local_path=local_path + "/" + filename,
                    file_name=data.get("folder", "default") + "/" + filename,
                    bucket="converter-logs"
                )
                print("file uploaded to s3: " + s3_path)
            except Exception as e:
                print("error uploading file to s3: " + str(e))

        return {"message": "Logs subidos a S3"}, 200
