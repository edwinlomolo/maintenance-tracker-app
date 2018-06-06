"""
Registration view
"""
import psycopg2

from flask import make_response, request, jsonify
from flask.views import MethodView
from models.user import User

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
            email = request.json.get('email', '')
            password = request.json.get('password', '')

            try:
                conn = psycopg2.connect(
                    host="localhost",
                    database="mtapi",
                    user="edwin",
                    password="47479031"
                )

                query = """SELECT EMAIL FROM USERS WHERE EMAIL = %s"""

                cur = conn.cursor()
                cur.execute(query, (email,))

                row = cur.fetchone()

                if row is not None:
                    return make_response(jsonify({
                        "error": "Email already taken. Please choose a different one."
                    })), 200
                user = User(email=email, password=password)
                user.save()
                return make_response(jsonify({
                    "message": "You are successfully registered. You can log in now."
                })), 201

            except(Exception, psycopg2.DatabaseError) as error: # pylint: disable=broad-except
                return make_response(jsonify({"message": str(error)}))
        else:
            return make_response(jsonify({"error": "Invalid input"})), 400

# API Resource
SIGN_UP = Registration.as_view("signup_view")
AUTH_BLUEPRINT.add_url_rule(
    "/api/v1.0/auth/signup/",
    view_func=SIGN_UP,
    methods=["POST"]
)
