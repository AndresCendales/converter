# Application Entrypoint

# Flask
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# App
from api import db

# Resources
from api.auth.views import LoginView, SignUpView
from api.tasks.views import TasksView, TaskView
from api.files.views import FilesView
from api.logs.views import LogsView


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.config['JWT_SECRET_KEY']='frase-secreta'
    app.config['PROPAGATE_EXCEPTIONS']=True

    # Initialize Plugins
    db.init_app(app)

    with app.app_context():
        # Include Routes
        api = Api(app)
        jwt = JWTManager(app)

        # Auth
        api.add_resource(LoginView, '/api/auth/login')
        api.add_resource(SignUpView, '/api/auth/signup', methods=['POST'])

        # Tasks
        app.add_url_rule('/api/tasks', view_func=TasksView.as_view("tasks_api"))
        app.add_url_rule('/api/tasks/<id_task>', view_func=TaskView.as_view("task_api"))

        # Files
        api.add_resource(FilesView, '/api/files/<filename>', methods=['GET'])

        # Logs
        api.add_resource(LogsView, "/api/logs", methods=['POST'])

        # Migration
        migrate = Migrate(app, db)

        return app
    
    