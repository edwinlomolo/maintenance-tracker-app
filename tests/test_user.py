"""
Tests for user
 ==> Signup
 ==> SignIn
 ==> Invalid credentials
 ==> Token generation
 ===> Token validation
"""
import unittest
import json
from app import create_app

class AuthenticationTestCases(unittest.TestCase):
    """
	User authentication test class
	"""
    def setUp(self):
        """
		Initialize test variable
		"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

    def test_user_can_register(self):
        """
        Test API can register a new user
        """
        # Send request
        res = self.client().post(
            "/api/v1.0/auth/signup/",
            json=dict(email="johndoe@email.com", password="4747")
        )
        # Get result and decode
        result = json.loads(res.data.decode())
        self.assertTrue(res.status_code, 201)
        self.assertEqual(
            str(result["message"]), "You have successfully registered, You can now log in."
        )

    def test_user_can_log_in(self):
        """
        Test API cana authenticate user
        """
        res = self.client().post(
            "/api/v1.0/auth/signin/",
            json=dict(email="johndoe@email.com", password="4747")
        )
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            str(result["message"]), "You logged in successfully."
        )
        self.assertIn(result["token"], "eY")
