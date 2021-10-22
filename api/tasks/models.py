# App
from app import db

# SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Task(db.Model):
    """Model for Users."""

    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    status = db.Column(db.String(25), nullable=False)
    new_format = db.Column(db.String, nullable=False)
    original_file_path = db.Column(db.String(256))
    new_file_path = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, nullable=False)


class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_relationships = False
        load_instance = True
