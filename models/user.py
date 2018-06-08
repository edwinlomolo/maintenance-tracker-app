"""
User model
"""
import os
from datetime import datetime, timedelta
import jwt
from flask_bcrypt import Bcrypt
from models.db import Db
from flask_bcrypt import Bcrypt
import psycopg2
from psycopg2.extras import RealDictCursor
import jwt

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
        query = """INSERT INTO USERS (email, password) VALUES(%s, %s)"""
        conn = None
        try:
            conn = psycopg2.connect(
                host=os.getenv("HOST"),
                database=os.getenv("DATABASE"),
                user=os.getenv("USER"),
                password=os.getenv("PASS")
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

    @staticmethod
    def query(user_id): # pylint: disable=no-self-use
        """
        Check if email is taken
        """
        db_connection = Db()
        is_taken = db_connection.email_taken(email)
        return is_taken

    def validate_password(self, password):
        query = """SELECT * FROM REQUESTS WHERE CREATED_BY = %s"""
        try:
            conn = psycopg2.connect(
                host=os.getenv("HOST"),
                database=os.getenv("DATABASE"),
                user=os.getenv("USER"),
                password=os.getenv("PASS")
            )

            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query, (user_id,))

            row = cur.fetchall()

            if row is not None:
                return row
            return None
        except(Exception, psycopg2.DatabaseError) as error: # pylint: disable=broad-except
            return error
    @staticmethod
    def validate_password(password1, password2):
        """
        Check if passwords provided match
        """
        return Bcrypt().check_password_hash(password1, password2)
    @staticmethod
    def generate_token(user_id): # pylint: disable=no-self-use
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
            return payload["user_id"]
        except jwt.ExpiredSignatureError:
            # if token is expired, probe our user to login to get a new one
            return "Expired token. Please login to get a new one."
        except jwt.InvalidTokenError:
            # if token is invalid, probe our user to register or login to get a new one.
            return "Invalid token. Please register or log in."
