# Views
from flask.views import MethodView


class FilesView(MethodView):
    def get(self, filename):
        """
        Get method of file view
        Retrieve a file by the filename
        :return:
        """
        # ToDo
        return f"Return file: {filename}"
