import unittest
import json
from app import create_app

class UserTestCase(unittest.TestCase):
	"""
	User class test cases
	"""
	def setUp(self):
		"""
		Initialize variables
		"""
		self.app = create_app(config_name="testing")
		self.client = self.app.test_client

	def test_api_can_create_user_account(self):
		"""
		Test API can create user account
		"""
		res = self.client().post("/users/api/v1.0/account/register/", json=dict(
			firstname="Edwin",
			lastname="Lomolo",
			email="edwin@gmail.com",
			password=1234,
			confirm_password=1234
		))
		data = json.loads(res.get_data(as_text=True))
		self.assertEqual(res.status_code, 201)
		self.assertEqual(str(data["message"]), "Your account was created successfully.")

	def test_api_can_log_in_user(self):
		"""
		Test API can login user
		"""
		res = self.client().post("/users/api/v1.0/authenticate/", json=dict(
			email="milly@gmail.com",
			password=4747
		))
		data = json.loads(res.get_data(as_text=True))
		self.assertEqual(res.status_code, 200)
		self.assertEqual(str(data["message"]), "Login was successfull")

if __name__ == '__main__':
	unittest.main()
