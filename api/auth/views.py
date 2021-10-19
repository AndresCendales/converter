# Flask
from flask_restful import Resource


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
        # ToDo
        return "SignUp resource"
