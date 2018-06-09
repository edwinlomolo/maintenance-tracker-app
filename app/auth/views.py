"""
Registration view
"""
import os
import psycopg2
from flask import make_response, request, jsonify
from flask.views import MethodView
from models.user import User
from validate_email import validate_email
from utils.validate_password import validate_password

from . import AUTH_BLUEPRINT

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
                                    email_is_taken = User.email_is_taken(email)
                                    username_is_taken = User.username_is_taken(username)
                                    if email_is_taken:
                                        return jsonify({"message": "Email is already taken. Please choose a different one"}), 202
                                    if username_is_taken:
                                        return jsonify({"message": "Username is already taken. Please choose a different one"}), 202
                                    user = User(firstname=firstname, lastname=lastname, email=email, username=username, password=password)
                                    user.save()
                                    return jsonify({"message": "Your account was successfully created"}), 201
                                return jsonify({
                                    "message": "Your password should be of 8 characters, contains an uppercase letter and lowercase letter, also and should contain a number or digit"
                                }), 202
                            return jsonify({"message": "Please provide a password"}), 202
                        return  jsonify({"message": "Please provide a username"}), 202
                    return jsonify({"message": "Please provide your email"}), 202
                return jsonify({"message": "Please provide your lastname"}), 202
            return jsonify({"message": "Please provide your firstname"}), 202
        return jsonify({
            "message": "Please provide your firstname, lastname, email, username, and password for sign up."
        }), 202

class Login(MethodView):
    """
    This class represents user signin view
    """
    def post(self): # pylint: disable=no-self-use
        """
        Handles post requests on this view
        """
        if request.json and request.json.get('email') and request.json.get('password'):

            # Get data from request
            email = request.json.get('email')
            password = request.json.get('password')

            # Try connecting to database
            try:
                conn = psycopg2.connect(
                    host=os.getenv("HOST"),
                    database=os.getenv("DATABASE"),
                    user=os.getenv("USER"),
                    password=os.getenv("PASS")
                )
                query = """SELECT ID, EMAIL, PASSWORD FROM USERS WHERE EMAIL = %s"""

                cur = conn.cursor()
                cur.execute(query, (email,))

                row = cur.fetchone()

                # Validate password
                if row is not None and User.validate_password(row[2], password):
                    # Send back token
                    return make_response(jsonify({
                        "message": "Logged in successfully.",
                        "token": User.generate_token(row[0])
                    })), 200
                # If wrong password or incorrect email address
                return make_response(jsonify({
                    "error": "Invalid email or password."
                })), 401
            except(Exception, psycopg2.DatabaseError) as error: # pylint: disable=broad-except
                return make_response(jsonify({
                    "error": str(error)
                })), 500
        else:
            # If request is empty
            return make_response(jsonify({
                "message": "Please provide both a valid email and password to log in."
            }))

# Define Signup Resource
SIGN_UP = Registration.as_view("signup_view")
AUTH_BLUEPRINT.add_url_rule(
    "/api/v1.0/auth/signup/",
    view_func=SIGN_UP,
    methods=["POST"]
)

# Define Signin Resource
SIGN_IN = Login.as_view("signin_view")
AUTH_BLUEPRINT.add_url_rule(
    "/api/v1.0/auth/signin/",
    view_func=SIGN_IN,
    methods=["POST"]
)
