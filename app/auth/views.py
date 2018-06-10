"""
Registration view
"""
from flask import request, jsonify
from flask.views import MethodView
from models.user import User
from validate_email import validate_email
from utils.validate_password import validate_password
from models.db import Db

from . import AUTH_BLUEPRINT

DB = Db()

class Registration(MethodView):
    """
    User registration view class
    """
    def post(self): # pylint: disable=no-self-use
        """
        Handle post requests on this view
        """
        if request.json:
            if request.json.get('firstname'):
                if request.json.get('lastname'):
                    if request.json.get('email'):
                        if request.json.get('username'):
                            if request.json.get('password'):
                                password = str(request.json.get('password'))
                                password_is_valid = validate_password(password)
                                if password_is_valid:
                                    firstname = str(request.json.get('firstname'))
                                    lastname = str(request.json.get('lastname'))
                                    email = str(request.json.get('email'))
                                    username = str(request.json.get('username'))
                                    password = str(request.json.get('password'))
                                    email_is_taken = DB.email_is_taken(email)
                                    username_is_taken = DB.username_is_taken(username)
                                    if email_is_taken:
                                        return jsonify({"message": "Email is already taken. Please choose a different one"}), 202
                                    if username_is_taken:
                                        return jsonify({"message": "Username is already taken. Please choose a different one"}), 202
                                    user = User(firstname=firstname, lastname=lastname, email=email, username=username, is_admin=False, password=password)
                                    user.save()
                                    return jsonify({"message": "Your account was successfully created"}), 201
                                return jsonify({
                                    "message": "Your password should be of 8 characters, contains an uppercase letter and lowercase letter, also and should contain a number or digit"
                                }), 202
                            return jsonify({"message": "Please provide a password"}), 400
                        return  jsonify({"message": "Please provide a username"}), 400
                    return jsonify({"message": "Please provide your email"}), 400
                return jsonify({"message": "Please provide your lastname"}), 400
            return jsonify({"message": "Please provide your firstname"}), 400
        return jsonify({
            "message": "Please provide your firstname, lastname, email, username, and password for sign up."
        }), 400

class Login(MethodView):
    """
    This class represents user signin view
    """
    def post(self): # pylint: disable=no-self-use
        """
        Handle post in this view
        """
        if request.json:
            if request.json.get('email'):
                if request.json.get('password'):
                    email = request.json.get('email')
                    password = request.json.get('password')
                    email_is_valid = validate_email(email)
                    if email_is_valid:
                        data = DB.filter_by_email(email)
                        if data is not None:
                            if User.validate_password(data["password"], password):
                                return jsonify({
                                    "message": "Logged in as {}".format(data["username"]),
                                    "token": User.generate_token(data)
                                }), 200
                            return jsonify({"message": "Invalid password"}), 401
                        return jsonify({"message": "No user with such email. Please register for an account."}), 404
                    return jsonify({"message": "Invalid email. Valid format is example@email.com"}), 400
                return jsonify({"message": "You need a password to login. Please, provide yours."}), 400
            return jsonify({"message": "You need an email to login. Please, provide yours."}), 400
        return jsonify({"message": "You need an email and password to login. Please, provide yours or register one."}), 400


# Define Signup Resource
SIGN_UP = Registration.as_view("signup_view")
AUTH_BLUEPRINT.add_url_rule(
    "/api/v1/auth/signup/",
    view_func=SIGN_UP,
    methods=["POST"]
)

# Define Signin Resource
SIGN_IN = Login.as_view("signin_view")
AUTH_BLUEPRINT.add_url_rule(
    "/api/v1/auth/signin/",
    view_func=SIGN_IN,
    methods=["POST"]
)
