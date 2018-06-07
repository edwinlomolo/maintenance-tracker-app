"""
Registration view
"""
import os
import psycopg2
from flask import make_response, request, jsonify
from flask.views import MethodView
from models.user import User
from validate_email import validate_email

from . import AUTH_BLUEPRINT

class Registration(MethodView):
    """
    User registration view class
    """
    def post(self): # pylint: disable=no-self-use
        """
        Handle post requests on this view
        """
        if request.json and request.json.get('email') and request.json.get('password'):

            # Get data from body
            email = request.json.get('email')
            password = request.json.get('password')
            is_valid = validate_email(email)

            if is_valid:
                # Try connecting to the database
                try:
                    conn = psycopg2.connect(
                        host=os.getenv("HOST"),
                        database=os.getenv("DATABASE"),
                        user=os.getenv("USER"),
                        password=os.getenv("PASS")
                    )
                    query = """SELECT EMAIL FROM USERS WHERE EMAIL = %s"""

                    # Get cursor object
                    cur = conn.cursor()
                    cur.execute(query, (email,))

                    row = cur.fetchone()

                    if row is not None:
                        return make_response(jsonify({
                            "message": "Email already taken. Please choose a different one."
                        })), 202
                    user = User(email=email, password=password)
                    user.save()
                    return make_response(jsonify({
                        "message": "You successfully registered. You can log in now."
                    })), 201
                except(Exception, psycopg2.DatabaseError) as error: # pylint: disable=broad-except
                    return make_response(jsonify({
                        "error": str(error)
                    })), 500
            else:
                return make_response(jsonify({
                    "error": "Invalid email address. Provide a valid email address."
                })), 400

        else:
            # If both email and password are not provided
            return make_response(jsonify({
                "error": "Please provide both an email and password."
            })), 400

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
