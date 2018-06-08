"""
Request model
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor

class Request(object): # pylint: disable=too-few-public-methods
    """
    Request class representation
    """

    def __init__(self, title, description, location, created_by): # pylint: disable=too-many-arguments
        self.title = title
        self.description = description
        self.location = location
        self.created_by = created_by

    def save(self):
        """
        Save request to the database
        """
        conn = None
        # Try connecting to the database
        try:
            conn = psycopg2.connect(
                host=os.getenv("HOST"),
                database=os.getenv("DATABASE"),
                user=os.getenv("USER"),
                password=os.getenv("PASS")
            )
            # Query for inserting data
            query = """
                    INSERT INTO 
                    REQUESTS (title, description, location, created_by)
                    VALUES (%s, %s, %s, %s)
                    """
            cur = conn.cursor()
            cur.execute(query, (self.title, self.description, self.location, self.created_by,))

            conn.commit()
            conn.close()
        except (Exception, psycopg2.DatabaseError) as error: # pylint: disable=broad-except
            print error
        finally:
            # Close connection if still open after query execution
            if conn is not None:
                conn.close()

    @staticmethod
    def get_request(user_id, request_id):
        """
        Fetch a request using its id
        """
        conn = None
        # Try connecting to the database
        try:
            conn = psycopg2.connect(
                host=os.getenv("HOST"),
                database=os.getenv("DATABASE"),
                user=os.getenv("USER"),
                password=os.getenv("PASS")
            )

            query = """
            SELECT ID, TITLE, DESCRIPTION, APPROVED, REJECTED, RESOLVED
            FROM REQUESTS WHERE CREATED_BY = %s AND ID = %s
            """

            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query, (user_id, request_id,))

            row = cur.fetchone()

            if row is not None:
                return row
            return None
        except(Exception, psycopg2.DatabaseError) as error: # pylint: disable=broad-except
            print error
        finally:
            if conn is not None:
                conn.close()
