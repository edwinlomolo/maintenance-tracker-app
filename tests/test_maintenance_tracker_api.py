"""
Test class for our Maintenance Tracker API endpoints
"""
import os
import unittest
from app import create_app

class MaintenanceTrackerTestCase(unittest.TestCase):
	"""
	Class for our maintenance tracker tests
	"""
	def setUp(self):
		"""
		Initialize our variable before test
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
		self.assertEqual(res.status_code, 201)
		self.assertTrue(str(res.data))

	def test_api_can_log_in_user(self):
		"""
		Test API can login user
		"""
		res = self.client().post("/users/api/v1.0/authenticate/", json=dict(
			email="milly@gmail.com",
			password=4747
		))
		self.assertEqual(res.status_code, 200)
		self.assertTrue(str(res.data))

	def test_api_can_create_a_request(self):
		"""
		Test API can create a request
		"""
		res = self.client().post("/users/api/v1.0/requests/", json=dict(
			title="Busted pipe",
			description="I have a leaking pipe in my sink and i have children in the house",
			location="Kisumu",
			create_by="Mike"
		))
		self.assertEqual(res.status_code, 201)
		self.assertTrue(res.data)

	def test_api_can_return_all_requests(self):
		"""
		Test API can return all requests created by a user
		"""
		res = self.client().get("/users/api/v1.0/requests/", headers=dict(name="Edwin"))
		self.assertEqual(res.status_code, 200)
		self.assertTrue(str(res.data))

	def test_api_can_return_a_request_create_by_a_user(self):
		"""
		Test API can return a request created by a user
		"""
		res = self.client().get("/users/api/v1.0/requests/{}/".format(2), headers=dict(name="Edwin"))
		self.assertEqual(res.status_code, 200)
		self.assertTrue(str(res.data))

	def test_api_can_edit_a_request(self):
		"""
		Test API can edit a request
		"""
		res = self.client().post("/users/api/v1.0/requests/{}/".format(3), json=dict(
			title="Broken window",
			description="My children can't sleep due to coldness. I have a broken window pane",
			location="Migori"
		), 
		headers=dict(name="Milly"))
		self.assertEqual(res.status_code, 200)
		self.assertTrue(str(res.data))

	def test_api_can_return_all_requests_for_admin(self):
		"""
		Test API can return all requests for admin
		"""
		res = self.client().get("/users/api/v1.0/requests/", headers=dict(name="admin"))
		self.assertEqual(res.status_code, 200)
		self.assertTrue(str(res.data))

	def test_api_can_edit_a_request_for_admin(self):
		"""
		Test API can allow request edit for admin
		"""
		res = self.client().post("/users/api/v1.0/requests/{}/".format(1), 
		json=dict(
			approved=False,
			rejected=True,
			resolved=True
		), headers=dict(name="admin"))
		self.assertEqual(res.status_code, 200)
		self.assertTrue(str(res.data))


if __name__ == '__main__':
	unittest.main()
		