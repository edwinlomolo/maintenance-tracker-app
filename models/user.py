"""
User model
"""
class User(object):
	"""
	User class representation
	"""

	def __init__(self, firstname, lastname, email, password):
		self.firstname = firstname
		self.lastname = lastname
		self.email = email
		self.password = password
