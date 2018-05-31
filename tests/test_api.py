"""
Test class for our Maintenance Tracker API endpoints
"""
import os
import unittest
import json
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
		data = json.loads(res.get_data(as_text=True))
		self.assertEqual(res.status_code, 201)
		self.assertIn("title", str(data))

	def test_api_can_return_all_requests(self):
		"""
		Test API can return all requests created by a user
		"""
		res = self.client().get("/users/api/v1.0/requests/", headers=dict(role="Edwin"))
		data = json.loads(res.get_data(as_text=True))
		self.assertEqual(res.status_code, 200)
		assert(len(str(data)) > 0)

	def test_api_can_return_a_request_created_by_a_user(self):
		"""
		Test API can return a request created by a user
		"""
		res = self.client().get("/users/api/v1.0/requests/{}/".format(2), headers=dict(role="Edwin"))
		data = json.loads(res.get_data(as_text=True))
		self.assertEqual(res.status_code, 200)
		assert(len(str(data)) > 0)

	def test_api_can_edit_a_request(self):
		"""
		Test API can edit a request
		"""
		res = self.client().post("/users/api/v1.0/requests/{}/".format(1), json=dict(
			title="Leakage",
			description="I have a busted pipe. Its leaking so bad.",
			location="Karen"
		), 
		headers=dict(role="Milly"))
		data = json.loads(res.get_data(as_text=True))
		self.assertEqual(res.status_code, 200)
		self.assertEqual(str(data["location"]), "Karen")

if __name__ == '__main__':
	unittest.main()
		