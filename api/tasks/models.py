# App
from app import db


class Task(db.Model):
    """Model for Users."""

    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(64), nullable=False)
    new_format = db.Column(db.String, nullable=False)
    status = db.Column(db.String(25), nullable=False)
    timestamp = db.Column(db.Date, nullable=False)
