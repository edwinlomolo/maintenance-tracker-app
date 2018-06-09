"""
Database connection class
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor

class Db(object):
    """
    Connection class represention class
    """
    def __init__(self):
        """
        Initialize database variable
        """
        try:
            self.connection = psycopg2.connect(
                host=os.getenv("HOST"),
                database=os.getenv("DATABASE"),
                user=os.getenv("USER"),
                password=os.getenv("PASS")
            )
        except psycopg2.DatabaseError as error:
            print error

    def save_new_user(self, firstname, lastname, email, username, password):
        """
        Save user to the database
        """
        query = """
        INSERT INTO USERS (firstname, lastname, email, username, password) VALUES (%s, %s, %s, %s, %s)
        """
        cur = self.connection.cursor()
        cur.execute(query, (firstname, lastname, email, username, password,))
        self.connection.commit()
        cur.close()

    def email_taken(self, email):
        """
        Get user email from the database
        """
        query = """SELECT EMAIL FROM USERS WHERE EMAIL = %s"""
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (email,))
        result = cur.fetchone()
        cur.close()
        if result is not None:
            return True
        return False

    def username_taken(self, username):
        """
        Get username from database
        """
        query = """SELECT USERNAME FROM USERS WHERE USERNAME = %s"""
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (username,))
        result = cur.fetchone()
        cur.close()
        if result is not None:
            return True
        return False

    def filter_requests_by_id(self, user_id):
        """
        Get data from db using id value
        """
        query = """SELECT * FROM REQUESTS WHERE CREATED_BY = %s"""
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (user_id,))
        result = cur.fetchall()
        cur.close()
        if len(result) >= 1:
            return result
        return None

    def create_table(self, query):
        """
        Create table
        """
        cur = self.connection.cursor()
        cur.execute(query)
        self.connection.commit()
        cur.close()

    def filter_by_email(self, email):
        """
        Get user from database using his/her email
        """
        query = """SELECT * FROM USERS WHERE EMAIL = %s"""
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (email,))
        result = cur.fetchone()
        cur.close()
        if result is not None:
            return result
        return None

