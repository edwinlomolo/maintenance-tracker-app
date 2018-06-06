"""
Create tables for user and requests
"""

import psycopg2

def create_tables():
    """
    Create tables into the database
	  """
    commands = (
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
		""",
   )

    conn = None
    try:
	    conn = psycopg2.connect(host="localhost", database="mtapi", user="edwin", password="47479031")
	    cur = conn.cursor()

	    for command in commands:
			    cur.execute(command)
		  cur.close()
		  conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
    	print(error)
    finally:
      if conn is not None:
			  conn.close()

if __name__ == '__main__':
	create_tables()
