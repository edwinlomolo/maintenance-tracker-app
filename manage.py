"""
Create tables for our database
"""
import os
import psycopg2

def create_tables():
    """
    Create users and requests table
    """
    tables = (
        """
        CREATE TABLE IF NOT EXISTS USERS (
          id SERIAL PRIMARY KEY,
          email VARCHAR(225) NOT NULL UNIQUE,
          is_admin VARCHAR(10) DEFAULT FALSE NOT NULL,
          password VARCHAR(225) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS REQUESTS (
          id SERIAL PRIMARY KEY,
          title VARCHAR(300) NOT NULL,
          description VARCHAR(500) NOT NULL,
          location VARCHAR(100) NOT NULL,
          approved BOOLEAN DEFAULT FALSE NOT NULL,
          rejected BOOLEAN DEFAULT FALSE NOT NULL,
          resolved BOOLEAN DEFAULT FALSE NOT NULL,
          created_by INTEGER NOT NULL,
          FOREIGN KEY (created_by) REFERENCES USERS (id) ON DELETE CASCADE
        )
        """
    )

    # Try connecting to the database
    try:
        conn = psycopg2.connect(
            host=os.getenv('HOST'),
            database=os.getenv('DATABASE'),
            user=os.getenv('USER'),
            password=os.getenv('PASS')
        )

        cur = conn.cursor()

        for table in tables:
            cur.execute(table)
        cur.close()
        conn.commit()
        conn.close()

    except(Exception, psycopg2.DatabaseError) as error: # pylint: disable=broad-except
        print error

if __name__ == '__main__':
    create_tables()
