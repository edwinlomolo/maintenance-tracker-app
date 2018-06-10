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

    def save_new_user(self, firstname, lastname, email, username, is_admin, password):
        """
        Save user to the database
        """
        query = """
        INSERT INTO USERS (firstname, lastname, email, username, is_admin, password) VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur = self.connection.cursor()
        cur.execute(query, (firstname, lastname, email, username, is_admin, password,))
        self.connection.commit()
        cur.close()

    def email_is_taken(self, email):
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

    def username_is_taken(self, username):
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

    def save_new_request(self, title, description, location, created_by):
        """
        Save request to the database
        """
        query = """INSERT INTO REQUESTS (title, description, location, created_by) VALUES (%s, %s, %s, %s)"""
        cur = self.connection.cursor()
        cur.execute(query, (title, description, location, created_by,))
        self.connection.commit()
        cur.close()

    def get_request_by_user_id(self, created_by):
        """
        Get a request using its id
        """
        query = """SELECT * FROM REQUESTS WHERE CREATED_BY = %s"""
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (created_by,))
        result = cur.fetchall()
        cur.close()
        if len(result) >= 1:
            return result
        return None

    def get_request_by_id(self, request_id, created_by):
        """
        Get request by id
        """
        query = """
        SELECT * FROM REQUESTS WHERE ID = %s AND CREATED_BY = %s"""
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (request_id, created_by,))
        result = cur.fetchone()
        cur.close()
        if result is not None:
            return result
        return None

    def update_request(self, title, description, location, approved, rejected, resolved, request_id, created_by):
        """
        Update request by its id
        """
        query = """UPDATE REQUESTS SET TITLE = %s, DESCRIPTION = %s, LOCATION = %s,
        APPROVED = %s, REJECTED = %s, RESOLVED = %s WHERE ID = %s AND CREATED_BY = %s"""
        cur = self.connection.cursor()
        cur.execute(query, (title, description, location, approved, rejected, resolved, request_id, created_by,))
        self.connection.commit()
        cur.close()

    def get_all(self):
        """
        Get all requests
        """
        query = """SELECT * FROM REQUESTS"""
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        if len(result) >= 1:
            return result
        return None

    def get_request(self, request_id):
        """
        Get a request by its id
        """
        query = """SELECT * FROM REQUESTS WHERE ID = %s"""
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (request_id,))
        result = cur.fetchone()
        cur.close()
        if result is not None:
            return result
        return None

    def approve_request(self, value, request_id):
        """
        Approve a request
        """
        query = """UPDATE REQUESTS SET APPROVED = %s, RESOLVED = 'Pending' WHERE ID = %s"""
        cur = self.connection.cursor()
        cur.execute(query, (value, request_id,))
        self.connection.commit()
        cur.close()

    def reject_request(self, value, request_id):
        """
        Reject a request
        """
        query = """UPDATE REQUESTS SET REJECTED = %s WHERE ID = %s"""
        cur = self.connection.cursor()
        cur.execute(query, (value, request_id,))
        self.connection.commit()
        cur.close()

    def resolve_request(self, value, request_id):
        """
        Resolve a request
        """
        query = """UPDATE REQUESTS SET RESOLVED = %s WHERE ID = %s"""
        cur = self.connection.cursor()
        cur.execute(query, (value, request_id,))
        self.connection.commit()
        cur.close()
