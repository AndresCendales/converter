# Application Entrypoint

# Flask
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

# App
from api import db

# Resources
from api.auth.views import LoginView, SignUpView
from api.tasks.views import TasksView, TaskView
from api.files.views import FilesView

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)

    with app.app_context():
        # Include Routes
        api = Api(app)

        # Auth
        api.add_resource(LoginView, '/api/auth/login', methods=['POST'])
        api.add_resource(SignUpView, '/api/auth/signup', methods=['POST'])

        # Tasks
        app.add_url_rule('/api/tasks', view_func=TasksView.as_view("tasks_api"))
        app.add_url_rule('/api/tasks/<id_task>', view_func=TaskView.as_view("task_api"))

        # Files
        api.add_resource(FilesView, '/api/files/<filename>', methods=['GET'])

        # Migration
        migrate = Migrate(app, db)

        return app