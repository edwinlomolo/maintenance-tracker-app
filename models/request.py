"""
Request model
"""
class Request(object):
	"""
	Request class representation
	"""

	def __init__(self, id, title, description, location, created_by):
		self.id = id
		self.title = title
		self.description = description,
		self.location = location
		self.created_by = created_by
