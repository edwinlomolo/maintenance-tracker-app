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

	def test_maintenance_tracker_can_get_a_request(self):
		"""
		Test API can return single request item
		"""
		res = self.client().get("/users/api/v1.0/requests/{}".format(2))
		self.assertEqual(res.status_code, 200)
		self.assertIn("title", str(res.data))

	def test_maintenance_tracker_api_can_get_all_requests(self):
		"""
		Test API can return all the requests
		"""
		res = self.client().get("/users/api/v1.0/requests/")
		self.assertEqual(res.status_code, 200)
		self.assertEqual(len(str(res.data)) == 1, msg="Should be alist of length 1")

	def test_maintenance_tracker_api_can_edit_a_request(self):
		"""
		Test APi can edit a single request
		"""
		res = self.client().put("/users/api/v1.0/requests/{}".format(2), {"approved": False})
		self.assertEqual(res.status_code, 200)
		rev = self.client().get("/users/api/v1.0/requests/{}".format(2))
		self.assertEqual(rev.status_code, 200)
		self.assertTrue(str(res.data["approved"]), msg="Approved should be True")

	def test_maintenance_tracker_api_can_create_requests(self):
		"""
		Test API can create a request
		"""
		res = self.client().post("/users/api/v1.0/requests/", {
			"id": 3,
			"title": "Broken tap",
			"description": "Overflow due to a broken tap. Can't close",
		})
		self.assertEqual(res.status_code, 201)
		rev = self.client().get("/users/v1.0/api/requests/{}".format(3))
		self.assertEqual(res.status_code, 200)
		self.assertTrue(str(res.data), msg="Response data should not be empty")

if __name__ == '__main__':
	unittest.main()
		