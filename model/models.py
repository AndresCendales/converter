from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(128))
  password = db.Column(db.String(128))
  email = db.Column(db.String(128))

class Task(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  timestamp = db.Column(db.DateTime)
  user_id = db.Column(db.Integer)
  status = db.Column(db.String(128))
  original_file_path = db.Column(db.String(256))
  new_format = db.Column(db.String(128))
  new_file_path = db.Column(db.String(128))
  

class UserSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = User
    include_relationships = False
    load_instance = True

class TaskSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Task
    include_relationships = False
    load_instance = True