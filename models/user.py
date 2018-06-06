"""
User model
"""
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
import jwt
from flask import current_app, jsonify
import psycopg2

class User(object):
    """
    User class representation
    """

    def __init__(self, email, password):
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def insert_user(self):
        """
        Save user to the database
        """
        query = """INSERT INTO USERS (email, password) VALUES(%s, %s)"""
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="mtapi",
                user="edwin",
                password="47479031"
            )
            cur = conn.cursor()
            cur.execute(query, (self.email, self.password,))

            conn.commit()
            conn.close()
        except(Exception, psycopg2.DatabaseError) as error: # pylint: disable=broad-except
            print error
        finally:
            if conn is not None:
                conn.close()

    def query(self, email): # pylint: disable=no-self-use
        """
        Query db for data
        """
        query = """SELECT EMAIL FROM USERS WHERE EMAIL = %s """
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="mtapi",
                user="host",
                password="47479031"
            )

            cur = conn.cursor()
            cur.execute(query, (email,))

            row = cur.fetchone()

            if row is not None:
                return jsonify(row)
            return "Not found"
        except:
            return "Encountered error"

    def validate_password(self, password):
        """
        Check if passwords provided match
        """
        return Bcrypt().check_password_hash(self.password, password)

    def generate_token(self, user_id):
        """
        Generate JWT token for access and authentication
        """
        try:
            # setup payload with an expiration date
            payload = {
                "exp": datetime.utcnow() + timedelta(minutes=60),
                "iat": datetime.utcnow(),
                "user_id": user_id
            }

            # create jwt token string using the secret key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get("SECRET_KEY"),
                algorithm="HS256"
            )
            return jwt_string
        except Exception as error: # pylint: disable=broad-except
            # return error as string
            return str(error)

    @staticmethod
    def decode_token(token):
        """
        Decode token string and validate
        """
        try:
            # try decoding using SECRET_KEY
            payload = jwt.decode(token, current_app.config.get("SECRET_KEY"))
            return payload["user_id"]
        except jwt.ExpiredSignatureError:
            # if token is expired, probe our user to login to get a new one
            return "Expired token. Please login to get a new one."
        except jwt.InvalidTokenError:
            # if token is invalid, probe our user to register or login to get a new one.
            return "Invalid token. Please register or log in."
