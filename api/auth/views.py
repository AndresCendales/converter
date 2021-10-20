# App
from app import db

# Flask
from flask_restful import Resource
from flask import request

# Models
from api.auth.models import User


class LoginView(Resource):
    def post(self):
        """
        Post method for LoginResource
        :return:
        """
        # ToDo
        return "Login Resource"


class SignUpView(Resource):
    def post(self):
        """
        Post method for SignUpResource
        :return:
        """
        data = request.json

        if data.get('password1') == data.get('password2'):
            new_user = User(
                username=data.get('username'),
                password=data.get('password1'),
                email=data.get('email')
            )

            db.session.add(new_user)
            db.session.commit()

            message = "user created"
            code = 201
        else:
            message = "user not created. verify the given paylaod."
            code = 400

        return {"message": message}, code
