# App
from app import db

# Views
from flask.views import MethodView
from flask import request

# Models
from api.tasks.models import Task

# Workers
from api.tasks.worker import celery

# Utils
from datetime import datetime


class TasksView(MethodView):
    """
    TasksView have the methods to handle all tasks
    """

    def post(self):
        """
        Post method of tasks view
        Create a new task.
        :return:
        """
        data = request.json

        new_task = Task(
            file_name=data.get('fileName', ''),
            new_format=data.get('newFormat', ''),
            status='uploaded',
            timestamp=datetime.now()
        )
        db.session.add(new_task)
        db.session.commit()

        celery.send_task('tasks.convert', args=[new_task.file_name, new_task.new_format], kwargs={})

        return {"message": "tarea creada"}, 200

    def get(self):
        """
        Post method of tasks view
        Retrieve all tasks
        :return:
        """
        # ToDo
        return "Return all Tasks"


class TaskView(MethodView):
    """
    TaskView have the methods to handle one task
    """

    def get(self, id_task):
        """
        Post method of tasks view
        Retrieve all tasks
        :return:
        """
        # ToDo
        return f"Return one task: {id_task}"

    def delete(self, id_task):
        """
        Post method of tasks view
        Create a new task.
        :return:
        """
        # ToDo
        return f"Delete one task: {id_task}"
