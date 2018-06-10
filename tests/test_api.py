"""
Tests cases for API
"""
import unittest
import json
from app import create_app
from models.db import Db

class TestCase(unittest.TestCase):
    """
	Class for API tests cases
	"""
    def setUp(self):
        """
        Initialize variables
        """
        self.app = create_app("testing")
        self.client = self.app.test_client

    def register_user(self, firstname="John", lastname="Doe", email="johndoe@gmail.com",
                      username="@john", is_admin=False, password="4747EdGr"):
        """
        Helper function to register user
        """
        return self.client().post(
            "/api/v1/auth/signup/",
            json=dict(firstname=firstname, lastname=lastname, email=email,
                      username=username, is_admin=is_admin, password=password)
        )

    def login_user(self, email="johndoe@gmail.com", password="4747EdGr"):
        """
        Helper function to login user
        """
        return self.client().post("/api/v1/auth/signin/",
                                  json=dict(email=email, password=password)
                                 )


    def test_api_can_create_request(self):
        """
        Test API can create new requests
        """
        self.register_user()
        user = self.login_user()
        user_token = json.loads(user.data.decode())["token"]

        res = self.client().post(
            "/api/v1/users/requests/",
            headers=dict(Authorization="Bearer " + user_token),
            json=dict(
                title="Dangerous cracked wall",
                description="I have a cracked wall in the apartment",
                location="Bungoma"
            )
        )
        self.assertEqual(res.status_code, 201)
        result = json.loads(res.data.decode())
        self.assertEqual(result["title"], "Dangerous cracked wall")

    def test_api_cannot_lack_request_title(self):
        """
        Test API can create request without request title
        """
        self.register_user()
        user = self.login_user()
        user_token = json.loads(user.data.decode())["token"]

        res = self.client().post(
            "/api/v1/users/requests/",
            headers=dict(Authorization="Bearer " + user_token),
            json=dict(
                description="I have a cracked wall in the apartment",
                location="Bungoma"
            )
        )
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result["message"], "Please provide the title, description, and location of your request.")
    def test_api_cannot_lack_request_description(self):
        """
        Test API can create request without request description
        """
        self.register_user()
        user = self.login_user()
        user_token = json.loads(user.data.decode())["token"]

        res = self.client().post(
            "/api/v1/users/requests/",
            headers=dict(Authorization="Bearer " + user_token),
            json=dict(
                title="Dangerous cracked wall",
                location="Bungoma"
            )
        )
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result["message"], "Please provide the title, description, and location of your request.")

    def test_api_cannot_lack_request_location(self):
        """
        Test API can create request without request location
        """
        self.register_user()
        user = self.login_user()
        user_token = json.loads(user.data.decode())["token"]

        res = self.client().post(
            "/api/v1/users/requests/",
            headers=dict(Authorization="Bearer " + user_token),
            json=dict(
                title="Dangerous cracked wall",
                description="I have a cracked wall in the apartment"
            )
        )
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result["message"], "Please provide the title, description, and location of your request.")

    def test_api_cannot_lack_request(self):
        """
        Test API can create request without request details
        """
        self.register_user()
        user = self.login_user()
        user_token = json.loads(user.data.decode())["token"]

        res = self.client().post(
            "/api/v1/users/requests/",
            headers=dict(Authorization="Bearer " + user_token)
        )
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result["message"], "Please provide the title, description, and location of your request.")

    def test_api_can_get_all_requests_for_user(self):
        """
        Test API can get all requests for logged in user
        """
        self.register_user()
        user = self.login_user()
        user_token = json.loads(user.data.decode())["token"]

        res = self.client().get("/api/v1/users/requests/", headers=dict(Authorization="Bearer " + user_token))
        self.assertEqual(res.status_code, 200)

    def test_api_can_not_edit_other_requests(self):
        """
        Test API cannot edit other users' requests
        """
        self.register_user()
        user = self.login_user()
        user_token = json.loads(user.data.decode())["token"]

        res = self.client().put(
            "/api/v1/users/requests/10/",
            headers=dict(Authorization="Bearer " + user_token),
            json=dict(
                title="Leaking roof",
                description="Leaking roof in our apartment",
                location="Eldoret"
            )
        )
        self.assertEqual(res.status_code, 401)
        result = json.loads(res.data.decode())
        self.assertEqual(result["message"], "Can't find request 10 created by you. You may not have the right access to that request.")

    def test_api_can_handle_empty_request(self):
        """
        Test API can handle empty json objects
        """
        self.register_user()
        user = self.login_user()
        user_token = json.loads(user.data.decode())["token"]

        res = self.client().put("/api/v1/users/requests/10/", headers=dict(Authorization="Bearer " + user_token))
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result["message"], "You only have the right access to edit your request title, description and location")


    def tearDown(self):
        """
        Clean database
        """
        DB = Db()
        DB.delete_by_email("johndoe@email.com")

if __name__ == '__main__':
    unittest.main()
