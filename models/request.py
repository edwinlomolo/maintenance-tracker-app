"""
Request model
"""
import os
import psycopg2

class Request(object): # pylint: disable=too-few-public-methods
    """
    Request class representation
    """

    def __init__(self, title, description, location, created_by): # pylint: disable=too-many-arguments
        self.title = title
        self.description = description,
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
