"""
Create tables for our database
"""
from models.db import Db

def create_tables():
    """
    Create users and requests table
    """
    tables = (
        """
        CREATE TABLE IF NOT EXISTS USERS (
          id SERIAL PRIMARY KEY,
          firstname VARCHAR(50) NOT NULL,
          lastname VARCHAR(50) NOT NULL,
          username VARCHAR(50) NOT NULL UNIQUE,
          email VARCHAR(50) NOT NULL UNIQUE,
          is_admin VARCHAR(10) DEFAULT FALSE NOT NULL,
          password VARCHAR(225) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS REQUESTS (
          id SERIAL PRIMARY KEY,
          title VARCHAR(100) NOT NULL,
          description VARCHAR(500) NOT NULL,
          location VARCHAR(50) NOT NULL,
          approved BOOLEAN DEFAULT FALSE NOT NULL,
          rejected BOOLEAN DEFAULT FALSE NOT NULL,
          resolved VARCHAR(50) DEFAULT FALSE NOT NULL,
          created_by INTEGER NOT NULL,
          FOREIGN KEY (created_by) REFERENCES USERS (id) ON DELETE CASCADE
        )
        """
    )

    # Try connecting to the database
    db_connection = Db()

    for table in tables:
        db_connection.create_table(table)

if __name__ == '__main__':
    create_tables()
