# App
from app import db

# Aws
from worker_sqs.send_messages import send_message, sqs

# config
from config import ALLOWED_EXTENSIONS

# Views
from flask.views import MethodView
from flask import request
from werkzeug.utils import secure_filename

# Flask
from flask_jwt_extended import jwt_required, get_jwt_identity

# Models
from api.tasks.models import Task, TaskSchema
from api.auth.models import User

# Validations
from api.tasks.validate import allowed_file

# Utils
from datetime import datetime
import os
from util import Logger, s3_service

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
        user = User.query.filter_by(username=get_jwt_identity()).first()
        
        file = request.files.get('fileName')
        
        if file is None:
            return {"message": "Por favor adjunta el archivo que deseas convertir"}, 400
        if file.filename == '':
            return {"message": "Filename invalido"}, 400
        file.filename = secure_filename(file.filename)
        if not allowed_file(file.filename):
            return {
                       "message": "Archivo no permitido. Las extensiones soportadas son {'mp3', 'acc', 'ogg', 'wav', 'wma'} "}, 400

        task = Task.query.filter_by(original_file_path=file.filename, user_id=user.id).first()
        if task is not None and os.getenv("APP_MODE") != "TEST":
            return {
                       "message": "Ya existe un archivo con este nombre. Para actualizar el formato se debe usar el endpoint via PUT",
                       "id_task": task.id}, 400

        new_format = request.form.get('newFormat')
        if new_format is None:
            return {"message": "Por favor incluye el formato al que deseas convertir"}, 400
        if new_format not in ALLOWED_EXTENSIONS:
            return {"message": "newFormat invalido, Las extensiones soportadas son {'mp3', 'acc', 'ogg', 'wav', 'wma'} "}, 400
        
        filename = str(user.id)+"/"+file.filename
        filepath = os.path.join(os.getenv("UPLOAD_FOLDER"), f"{user.id}/" + file.filename)
        os.system(f"mkdir -p files/{user.id}")
        file.save(filepath)
        s3_path = s3_service.s3_upload_file(filepath, filename)
        logger.info('TasksView', 'post', 'guardado en la ruta ' + s3_path + ' de s3')

        new_task = Task(
            user_id=user.id,
            status='uploaded',
            new_format=new_format,
            original_file_path=file.filename,
            new_file_path="",
            timestamp=datetime.utcnow()
        )
        db.session.add(new_task)
        db.session.flush()
        db.session.refresh(new_task)
        db.session.commit()

        send_message(
            queue=sqs.get_queue_by_name(QueueName="conversiones"),
            message_body=f"Nueva Tarea de actualizacion de formato del archivo {new_task.original_file_path} al formato {new_format}",
            message_attributes={
                "user_id": {'StringValue': str(user.id), 'DataType': 'String'},
                "original_filename": {'StringValue': new_task.original_file_path, 'DataType': 'String'},
                "new_format": {'StringValue': new_format, 'DataType': 'String'},
                "created_at": {'StringValue': str(datetime.now()), 'DataType': 'String'},
                "filename_to_delete": {'StringValue': " " + new_task.new_file_path, 'DataType': 'String'},
                "s3_path": {'StringValue': s3_path, 'DataType': 'String'},
            }
        )

        return {"message": "tarea creada satisfactoriamente.", "id_task": new_task.id}, 200

    @jwt_required()
    def get(self):
        """
        Post method of tasks view
        Retrieve all tasks
        :return:
        """
        try:
            user = User.query.filter_by(username=get_jwt_identity()).first()
            max = request.args.get('max') or None
            if max == '0':
                max = None

            order = request.args.get('order', '0') or 0
            query_order = Task.id.asc() if order == '0' else Task.id.desc()

            tasks = Task.query.filter_by(user_id=user.id).order_by(query_order).limit(max).all()
            if len(tasks) == 0:
                logger.info('TasksView', 'get', 'Consulta de tareas sin resultado')
                return {"mensaje": 'El usuario no tiene tareas'}, 400
            serialized_tasks = [task_schema.dump(task) for task in tasks]
            logger.info('TasksView', 'get', 'Consulta de tareas exitosa')
            return {'tasks': serialized_tasks}, 200
        except Exception as err:
            print(err)
            logger.error('TasksView', 'get', 'error al consultar las tareas: ' + err)
            return {'mensaje': 'server error'}, 500


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
        user = User.query.filter_by(username=get_jwt_identity()).first()
        try:
            task = Task.query.get(id_task)
            if task is None:
                logger.info('TaskView', 'get', 'Tarea no encontrada')
                return {'mensaje': 'Tarea no encontrada'}, 404
            if task.user_id != user.id:
                logger.info('TaskView', 'get', 'Tarea de otro usuario')
                return {'mensaje': 'Tarea de otro usuario'}, 401

            logger.info('TaskView', 'get', 'Tarea encontrada')
            return task_schema.dump(task), 200
        except:
            logger.error('TaskView', 'get', 'error al consultar las tareas')
            return {'mensaje': 'server error'}, 500

    @jwt_required()
    def put(self, id_task):
        """
        Put method of tasks view
        Update a task
        :return:
        """
        data = request.json

        new_format = data.get('newFormat')
        if new_format is None:
            return {"mensaje": "Debe enviar el nuevo formato al cual desea convertir el archivo."}, 400

        if new_format not in ALLOWED_EXTENSIONS:
            return {
                       "message": "newFormat invalido, Las extensiones soportadas son {'mp3', 'acc', 'ogg', 'wav', 'wma'} "}, 400

        task = Task.query.filter_by(id=id_task).first()
        if task is None:
            return {"mensaje": "La tarea no existe"}, 404
        if (task.new_format == new_format or task.original_file_path.rsplit('.', 1)[1] == new_format) and os.getenv("APP_MODE") != "TEST" :
            return {"mensaje": f"La conversion hacia el formato {new_format} ya ha sido realizada."}, 400

        task.status = "uploaded"
        task.new_format = new_format
        db.session.commit()

        user = User.query.filter_by(username=get_jwt_identity()).first()
        s3_path = "files/"+str(user.id)+"/"+task.original_file_path
        logger.info('TaskView', 'put', 'buscar en la ruta ' + s3_path + ' de s3')

        send_message(
            queue=sqs.get_queue_by_name(QueueName="conversiones"),
            message_body=f"Nueva Tarea de actualizacion de formato del archivo {task.original_file_path} al formato {new_format}",
            message_attributes={
                "user_id": {'StringValue': str(user.id), 'DataType': 'String'},
                "original_filename": {'StringValue': task.original_file_path, 'DataType': 'String'},
                "new_format": {'StringValue': new_format, 'DataType': 'String'},
                "created_at": {'StringValue': str(datetime.now()), 'DataType': 'String'},
                "filename_to_delete": {'StringValue': " " + task.new_file_path, 'DataType': 'String'},
                "s3_path": {'StringValue': s3_path, 'DataType': 'String'},
            }
        )
        return {"mensaje": "Se ha actualizado la tarea", "id_task": task.id}

    @jwt_required()
    def delete(self, id_task):
        """
        Post method of tasks view
        Create a new task.
        :return:
        """
        user = User.query.filter_by(username=get_jwt_identity()).first()

        task = Task.query.filter_by(id=id_task, user_id=user.id).first()
        if task is None:
            logger.info('TaskView', 'get', 'Tarea no encontrada')
            return {'mensaje': 'tarea no encontrada'}, 404

        if task.status == 'processed':
            os.system(f"rm -rf files/{user.id}/{task.original_file_path}")
            db.session.delete(task)
            db.session.commit()

        return "", 200
