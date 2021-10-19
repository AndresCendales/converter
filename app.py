# Application Entrypoint

# Flask
from flask import Flask
from flask_restful import Api

# Resources
from api.auth.views import LoginView, SignUpView
from api.tasks.views import TasksView, TaskView
from api.files.views import FilesView

# Utils
import os

app = Flask(__name__)
api = Api(app)

# Auth
api.add_resource(LoginView, '/api/auth/login', methods=['POST'])
api.add_resource(SignUpView, '/api/auth/signup', methods=['POST'])

# Tasks
app.add_url_rule('/api/tasks', view_func=TasksView.as_view("tasks_api"))
app.add_url_rule('/api/tasks/<id_task>', view_func=TaskView.as_view("task_api"))

# Files
api.add_resource(FilesView, '/api/files/<filename>', methods=['GET'])
