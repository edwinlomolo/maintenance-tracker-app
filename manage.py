import psycopg2

def create_tables():
	"""
	Create tables into the database
	"""
	commands = (
		"""
		CREATE TABLE USERS (
			id SERIAL PRIMARY KEY,
			email VARCHAR(225) NOT NULL,
			password VARCHAR(225) NOT NULL
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
