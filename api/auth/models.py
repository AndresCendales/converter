# App
from enum import unique
from app import db

# SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class User(db.Model):
    """Model for Users."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(25), nullable=False, unique=True)


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = False
        load_instance = True
