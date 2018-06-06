"""
Registration view
"""
import psycopg2

from flask import make_response, request, jsonify, abort
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
        email = request.json.get('email', '')
        user = User.query(email)

        if user is None:
            return jsonify({ "massage": "User not found"})
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="mtapi",
                user="edwin",
                password="47479031"
            )
            query = """SELECT EMAIL FROM USERS WHERE EMAIL = %s """

            cur = conn.cursor()
            cur.execute(query, (email,))
            row = cur.fetchone()

            if row is not None:
                return jsonify(row)
            return jsonify({ "message": "Empty data" })
        except(Exception, psycopg2.DatabaseError) as error: # pylint: disable=broad-except
            return jsonify({ "message": str(error) })

SIGN_UP = Registration.as_view("signup_view")
AUTH_BLUEPRINT.add_url_rule(
    "/api/v1.0/auth/signup/",
    view_func=SIGN_UP,
    methods=["POST"]
)
