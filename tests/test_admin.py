import unittest
import json
from app import create_app

class AdminTestCase(unittest.TestCase):
	"""
	Admin test cases
	"""
	def setUp(self):
		"""
		Initialize variables
		"""
		self.app = create_app(config_name="testing")
		self.client = self.app.test_client

	def test_api_can_return_all_requests_for_admin(self):
		"""
		Test API can return all requests for admin
		"""
		res = self.client().get("/admin/api/v1.0/requests/", headers=dict(role="admin"))
		data = json.loads(res.get_data(as_text=True))
		self.assertEqual(res.status_code, 200)
		assert(len(str(data)) > 0)

	def test_api_can_edit_a_request_for_admin(self):
		"""
		Test API can allow request edit for admin
		"""
		res = self.client().post("/admin/api/v1.0/requests/{}/".format(1), 
		json=dict(
			resolved=True
		), headers=dict(role="admin"))
		data = json.loads(res.get_data(as_text=True))
		self.assertEqual(res.status_code, 200)
		self.assertEqual(data["resolved"], True)

	def test_api_can_return_single_request_for_admin(self):
		"""
		Test API can get a request for admin
		"""
		res = self.client().get("/admin/api/v1.0/requests/{}/".format(1), headers=dict(role="admin"))
		self.assertEqual(res.status_code, 200)
		data = json.loads(res.get_data(as_text=True))
		self.assertEqual(int(data["id"]), 1)

	def test_api_can_return_error_for_unauthorized_request(self):
		"""
		Test API can return error for unauthorized request
		"""
		res = self.client().get("/admin/api/v1.0/requests/", headers=dict(role="Mike"))
		data = json.loads(res.get_data(as_text=True))
		self.assertEqual(res.status_code, 401)
		self.assertEqual(str(data["error"]), "Unauthorized")

if __name__ == '__main__':
	unittest.main()