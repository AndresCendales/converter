# App
from app import db

# Views
from flask.views import MethodView
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

# Models
from api.tasks.models import Task, TaskSchema

# Workers
from api.tasks.worker import celery

# Utils
from datetime import datetime
from util import Logger

task_schema = TaskSchema()
logger = Logger()


class TasksView(MethodView):
    """
    TasksView have the methods to handle all tasks
    """
    @jwt_required()
    def post(self):
        """
        Post method of tasks view
        Create a new task.
        :return:
        """
        data = request.json

        new_task = Task(
            original_file_path=data.get('fileName', ''),
            new_file_path="NEW",
            new_format=data.get('newFormat', ''),
            status='uploaded',
            timestamp=datetime.utcnow()
        )
        db.session.add(new_task)
        db.session.commit()

        celery.send_task('tasks.convert', args=[new_task.original_file_path, new_task.new_format], kwargs={})

        return {"message": "tarea creada"}, 200

    @jwt_required()
    def get(self):
        """
        Post method of tasks view
        Retrieve all tasks
        :return:
        """
        try:
            # TODO: actualizar con el id de usuario desde el token
            user_id = get_jwt_identity()
            max = request.args.get('max') or None
            if (max == '0'):
                max = None
            order = request.args.get('order') or 0
            query_order = Task.id.asc() if order == '0' else Task.id.desc()
            tasks = Task.query.filter_by(user_id = user_id).order_by(query_order).limit(max).all()
            if (len(tasks) == 0):
                logger.info('TasksView', 'get', 'Consulta de tareas sin resultado')
                return 'El usuario no tiene tareas', 400
            serialized_tasks = [task_schema.dump(task) for task in tasks]
            logger.info('TasksView', 'get', 'Consulta de tareas exitosa')
            return {'tasks': serialized_tasks}, 200
        except Exception as err:
            print(err)
            logger.error('TasksView', 'get', 'error al consultar las tareas: ' + err)
            return {'msg': 'server error'}, 500


class TaskView(MethodView):
    """
    TaskView have the methods to handle one task
    """
    @jwt_required()
    def get(self, id_task):
        """
        Post method of tasks view
        Retrieve all tasks
        :return:
        """
        # TODO: actualizar con el token del usuario
        user_id = get_jwt_identity()
        try:
            task = Task.query.get(id_task)
            if task is None:
                logger.info('TaskView', 'get', 'Tarea no encontrada')
                return {'task': 'not found'}, 404

            logger.info('TaskView', 'get', 'Tarea encontrada')
            return task_schema.dump(task), 200
        except:
            logger.error('TaskView', 'get', 'error al consultar las tareas')
            return {'msg': 'server error'}, 500

    @jwt_required()
    def delete(self, id_task):
        """
        Post method of tasks view
        Create a new task.
        :return:
        """
        # ToDo
        return f"Delete one task: {id_task}"
