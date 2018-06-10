"""
User model
"""
import os
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
import jwt
from models.db import Db

DB = Db()

class User(object):
    """
    User class representation
    """

    def __init__(self, firstname, lastname, email, username, is_admin, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.is_admin = is_admin
        self.password = Bcrypt().generate_password_hash(password).decode()

    def save(self):
        """
        Save user to the database
        """
        DB.save_new_user(self.firstname, self.lastname, self.email,
                         self.username, self.is_admin, self.password)

    @staticmethod
    def filter_requests_by_user_id(user_id): # pylint: disable=no-self-use
        """
        Get request data created by user
        """
        result = DB.filter_requests_by_id(user_id)
        return result

    @staticmethod
    def email_is_taken(email):
        """
        Check if email is taken
        """
        is_taken = DB.email_is_taken(email)
        return is_taken

    @staticmethod
    def username_is_taken(username):
        """
        Check if username is taken
        """
        is_taken = DB.username_is_taken(username)
        return is_taken

    @staticmethod
    def validate_password(password1, password2):
        """
        Check if passwords provided match
        """
        return Bcrypt().check_password_hash(password1, password2)
    @staticmethod
    def generate_token(data): # pylint: disable=no-self-use
        """
        Generate JWT token for access and authentication
        """
        try:
            # setup payload with an expiration date
            payload = {
                "exp": datetime.utcnow() + timedelta(minutes=60),
                "iat": datetime.utcnow(),
                "user": {
                    "id": data["id"],
                    "is_admin": data["is_admin"]
                }
            }

            # create jwt token string using the secret key
            jwt_string = jwt.encode(
                payload,
                os.getenv("SECRET_KEY"),
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
            payload = jwt.decode(token, os.getenv("SECRET_KEY"))
            return payload["user"]
        except jwt.ExpiredSignatureError:
            # if token is expired, probe our user to login to get a new one
            return "Expired token. Please login to get a new one."
        except jwt.InvalidTokenError:
            # if token is invalid, probe our user to register or login to get a new one.
            return "Invalid token. Please register or log in."
