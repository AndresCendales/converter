# Views
from flask.views import MethodView
from flask import request

from model import Task, TaskSchema
from util import Logger

task_schema = TaskSchema()
logger = Logger()

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
        # ToDo
        return "Create new task"

    def get(self):
        """
        Post method of tasks view
        Retrieve all tasks
        :return:
        """
        try:
            # TODO: actualizar con el id de usuario desde el token
            max = request.args.get('max') or None
            if (max == '0'):
                max = None
            order = request.args.get('order') or 0
            query_order = Task.id.asc() if order == '0' else Task.id.desc()
            tasks = Task.query.filter_by(user_id = 1).order_by(query_order).limit(max).all()
            if (len(tasks) == 0):
                logger.info('TasksView', 'get', 'Consulta de tareas sin resultado')
                return 'El usuario no tiene tareas', 400
            serialized_tasks = [task_schema.dump(task) for task in tasks]
            logger.info('TasksView', 'get', 'Consulta de tareas exitosa')
            return  { 'tasks': serialized_tasks } , 200
        except Exception as err:
            print(err)
            logger.error('TasksView', 'get', 'error al consultar las tareas: ' + err)
            return { 'msg': 'server error' }, 500


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
        # TODO: actualizar con el token del usuario
        try:
            task = Task.query.get(id_task)
            if (task is None):
                logger.info('TaskView', 'get', 'Tarea no encontrada')
                return  { 'task': 'not found' } , 404
                
            logger.info('TaskView', 'get', 'Tarea encontrada')
            return task_schema.dump(task), 200
        except:
            logger.error('TaskView', 'get', 'error al consultar las tareas')
            return { 'msg': 'server error' }, 500

    def delete(self, id_task):
        """
        Post method of tasks view
        Create a new task.
        :return:
        """
        # ToDo
        return f"Delete one task: {id_task}"
