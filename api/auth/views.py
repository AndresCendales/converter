# App
from app import db

# Flask
from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token

# Models
from api.auth.models import User

# Utils
import os
import re


class LoginView(Resource):
    def post(self):
        """
        Post method for LoginResource
        :return:
        """
        data = request.json
        if (data == None or data.get('username') == None or data.get('password') == None):
            return {"message": "please send the values for the request."}, 400

        user_by_name = User.query.filter_by(username=data.get('username')).first()
        if (user_by_name == None):
            return {"message": "user isn't registered."}, 400
        if (user_by_name.password.strip() != data.get('password').strip()):
            return {"message": "error with login."}, 400

        access_token = create_access_token(identity=user_by_name.username)
        return {"message": "user logged", "access_token": access_token}, 200


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

        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$"
        pat = re.compile(reg)
        mat = re.search(pat, data.get('password1').strip())
        
        if not mat:
            return {"message": "user not created. password doesn't meet the security requirements."}, 400

        user_by_name = User.query.filter_by(username=data.get('username')).first()
        if (user_by_name != None):
            return {"message": "user not created. username in use."}, 400

        user_by_email = User.query.filter_by(email=data.get('email')).first()
        if (user_by_email != None):
            return {"message": "user not created. email in use."}, 400

        new_user = User(
            username=data.get('username').strip(),
            password=data.get('password1').strip(),
            email=data.get('email').strip()
        )

        access_token = create_access_token(identity=data.get('username').strip())

        db.session.add(new_user)
        db.session.flush()
        db.session.refresh(new_user)
        db.session.commit()

        os.system(f"mkdir files/{new_user.id}")

        return {"message": "user created", "access_token": access_token}, 201
