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

# Define API Resource
SIGN_UP = Registration.as_view("signup_view")
AUTH_BLUEPRINT.add_url_rule(
    "/api/v1.0/auth/signup/",
    view_func=SIGN_UP,
    methods=["POST"]
)
