# App
from os import access
from sqlalchemy.orm import query
from api.notificator.notifier import Notifier
from app import db

# Flask
from flask_restful import Resource
from flask import request,jsonify, make_response
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

# Models
from api.auth.models import User


class LoginView(Resource):
    def post(self):
        """
        Post method for LoginResource
        :return:
        """
        data = request.json
        if (data == None or data.get('username') == None or data.get('password') == None):
            return {"message": "please send the values for the request."}, 400

        user_by_name = User.query.filter_by(username = data.get('username')).first()
        if (user_by_name == None):
            return {"message": "user isn't registered."}, 400
        if (user_by_name.password.strip() != data.get('password').strip()):
            return {"message": "error with login."}, 400
        
        access_token = create_access_token(identity=user_by_name.username)
        return {"message": "user logged", "access_token": access_token}, 200

    @jwt_required()
    def get(self):
        username = get_jwt_identity()

        notifier = Notifier()
        notifier.send_notification_to_download(username, "/original-file-path.txt","pdf", "/new-file-path.pdf")
        return 'hola '+username, 200

class SignUpView(Resource):
    def post(self):
        """
        Post method for SignUpResource
        :return:
        """
        data = request.json
        if (data == None or data.get('username') == None or data.get('password1') == None 
        or data.get('password2') == None or data.get('email') == None):
            return {"message": "please send the values for the request."}, 400

        if data.get('password1') != data.get('password2'):
            return {"message": "user not created. passwords don't match."}, 400
        
        user_by_name = User.query.filter_by(username = data.get('username')).first()
        if (user_by_name != None):
            return {"message": "user not created. username in use."}, 400

        user_by_email = User.query.filter_by(email = data.get('email')).first()
        if (user_by_email != None):
            return {"message": "user not created. email in use."}, 400

        new_user = User(
            username=data.get('username').strip(),
            password=data.get('password1').strip(),
            email=data.get('email').strip()
        )

        db.session.add(new_user)
        db.session.commit()           

        return {"message": "user created"}, 201
