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
        self.connection.close()

    def email_taken(self, email):
        """
        Get user email from the database
        """
        query = """SELECT EMAIL FROM USERS WHERE EMAIL = %s"""
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (email,))
        result = cur.fetchone()
        cur.close()
        self.connection.close()
        if result is not None:
            return True
        return False

    def create_table(self, query):
        """
        Create table
        """
        cur = self.connection.cursor()
        cur.execute(query)
        self.connection.commit()
        cur.close()
