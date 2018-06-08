"""
User model
"""
from datetime import datetime, timedelta
import jwt
from flask_bcrypt import Bcrypt
from models.db import Db

class User(object):
    """
    User class representation
    """

    def __init__(self, firstname, lastname, username, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def save(self):
        """
        Save user to database
        """
        db_connection = Db()
        db_connection.save_new_user(self.firstname, self.lastname, self.email, self.username, self.password)

    @staticmethod
    def email_is_taken(email):
        """
        Check if email is taken
        """
        db_connection = Db()
        is_taken = db_connection.email_taken(email)
        return is_taken

    def validate_password(self, password):
        """
        Check if passwords provided match
        """
        return Bcrypt().check_password_hash(self.password, password)

    def generate_token(self, user_id): # pylint: disable=no-self-use
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
