"""
Request model
"""
from models.db import Db

DB = Db()

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
        DB.save_new_request(self.title, self.description, self.location, self.created_by)
