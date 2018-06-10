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
from models.db import Db

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
            "/api/v1/auth/signup/",
            json=dict(firstname="John", lastname="Doe",
                      email="johndoe@email.com", username="@edwin",
                      is_admin=False, password="4747EdGr")
        )
        # Get result and decode
        result = json.loads(res.data.decode())
        self.assertTrue(res.status_code, 201)
        self.assertEqual(
            str(result["message"]), "Your account was successfully created"
        )

    def test_account_duplication(self):
        """
        Test API can handle email duplication error
        """
        res = self.client().post(
            "/api/v1/auth/signup/",
            json=dict(firstname="John", lastname="Doe",
                      email="johndoe@email.com", username="@edwin",
                      is_admin=False, password="4747EdGr")
        )
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post(
            "/api/v1/auth/signup/",
            json=dict(firstname="John", lastname="Doe",
                      email="johndoe@email.com", username="@edwin",
                      is_admin=False, password="4747EdGr")
        )
        result = json.loads(second_res.data.decode())
        self.assertEqual(second_res.status_code, 202)
        self.assertEqual(
            str(result["message"]), "Email is already taken. Please choose a different one"
        )

    def test_username_duplication(self):
        """
        Test API can handle username duplication
        """
        res = self.client().post(
            "/api/v1/auth/signup/",
            json=dict(firstname="John", lastname="Doe",
                      email="johndoe@email.com", username="@edwin",
                      is_admin=False, password="4747EdGr")
        )
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post(
            "/api/v1/auth/signup/",
            json=dict(firstname="Jane", lastname="Doe",
                      email="janedoe@email.com", username="@edwin",
                      is_admin=False, password="4747EdGr")
        )
        result = json.loads(second_res.data.decode())
        self.assertEqual(second_res.status_code, 202)
        self.assertEqual(
            str(result["message"]), "Username is already taken. Please choose a different one"
        )

    def test_password_validation(self):
        """
        Test API can validate password
        """
        res = self.client().post(
            "/api/v1/auth/signup/",
            json=dict(firstname="John", lastname="Doe",
                      email="johndoe@email.com", username="@edwin",
                      is_admin=False, password="47EdGr")
        )
        self.assertEqual(res.status_code, 202)
        result = json.loads(res.data.decode())
        self.assertEqual(
            str(result["message"]), "Your password should be of 8 characters, contains an uppercase letter and lowercase letter, also and should contain a number or digit"
        )


    def test_signup_input(self):
        """
        Test API can handle empty requests during signup
        """
        res = self.client().post("/api/v1/auth/signup/")
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            str(result["message"]), "Please provide your firstname, lastname, email, username, and password for sign up."
        )

    def test_firstname_signup(self):
        """
        Test API can handle orphaned input during signup
        """
        res = self.client().post(
            "/api/v1/auth/signup/",
            json=dict(lastname="Doe",
                      email="johndoe@email.com", username="@edwin",
                      is_admin=False, password="4747EdGr")
        )
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            str(result["message"]), "Please provide your firstname"
        )

    def test_lastname_signup(self):
        """
        Test API can handle orphaned input during signup
        """
        res = self.client().post(
            "/api/v1/auth/signup/",
            json=dict(firstname="John", email="johndoe@email.com", username="@edwin",
                      is_admin=False, password="4747EdGr")
        )
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            str(result["message"]), "Please provide your lastname"
        )

    def test_username_signup(self):
        """
        Test API can handle orphaned input during signup
        """
        res = self.client().post(
            "/api/v1/auth/signup/",
            json=dict(firstname="John", lastname="Doe",
                      email="johndoe@email.com", is_admin=False, password="4747EdGr")
        )
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            str(result["message"]), "Please provide a username"
        )

    def test_email_signup(self):
        """
        Test API can handle orphaned input during signup
        """
        res = self.client().post(
            "/api/v1/auth/signup/",
            json=dict(firstname="John", lastname="Doe", username="@edwin",
                      is_admin=False, password="4747EdGr")
        )
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            str(result["message"]), "Please provide your email"
        )

    def test_password_signup(self):
        """
        Test API can handle orphaned input during signup
        """
        res = self.client().post(
            "/api/v1/auth/signup/",
            json=dict(firstname="John", lastname="Doe",
                      email="johndoe@email.com", username="@edwin",
                      is_admin=False)
        )
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            str(result["message"]), "Please provide a password"
        )

    def test_user_can_log_in(self):
        """
        Test API can authenticate user
        """
        res = self.client().post(
            "/api/v1/auth/signup/",
            json=dict(firstname="John", lastname="Doe",
                      email="johndoe@email.com", username="@edwin",
                      is_admin=False, password="4747EdGr")
        )
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post(
            "/api/v1/auth/signin/",
            json=dict(email="johndoe@email.com", password="4747EdGr")
        )
        result = json.loads(second_res.data.decode())
        self.assertEqual(second_res.status_code, 200)
        self.assertEqual(
            str(result["message"]), "Logged in as @edwin"
        )
        self.assertIn("ey", str(result["token"]))

    def test_signin_with_unregistered_email(self):
        """
        Test API can handle unregistered email
        """
        res = self.client().post(
            "/api/v1/auth/signup/",
            json=dict(firstname="John", lastname="Doe",
                      email="johndoe@email.com", username="@edwin",
                      is_admin=False, password="4747EdGr")
        )
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post(
            "/api/v1/auth/signin/",
            json=dict(email="janedoe@email.com", password="4747EdGr")
        )
        result = json.loads(second_res.data.decode())
        self.assertEqual(second_res.status_code, 404)
        self.assertEqual(
            str(result["message"]), "No user with such email. Please register for an account."
        )

    def test_unauthorized_access(self):
        """
        Test API can handle unauthorized access
        """

        res = self.client().post(
            "/api/v1/auth/signup/",
            json=dict(firstname="John", lastname="Doe",
                      email="johndoe@email.com", username="@edwin",
                      is_admin=False, password="4747EdGr")
        )
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post(
            "/api/v1/auth/signin/",
            json=dict(email="johndoe@email.com", password="4745EdGr")
        )
        result = json.loads(second_res.data.decode())
        self.assertEqual(second_res.status_code, 401)
        self.assertEqual(
            str(result["message"]), "Invalid password"
        )
    def test_signin_input(self):
        """
        Test API can handle empty requests during signin
        """
        res = self.client().post("/api/v1/auth/signin/")
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            str(result["message"]), "You need an email and password to login. Please, provide yours or register one."
        )

    def test_no_email_provided(self):
        """
        Test API can handle no email input
        """
        res = self.client().post("/api/v1/auth/signin/", json=dict(password="4747EdGr"))
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            str(result["message"]), "You need an email to login. Please, provide yours."
        )

    def test_no_password_provided(self):
        """
        Test API can handle no email input
        """
        res = self.client().post("/api/v1/auth/signin/", json=dict(email="johndoe@email.com"))
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            str(result["message"]), "You need a password to login. Please, provide yours."
        )

    def test_invalid_email(self):
        """
        Test API can handle orphaned email input during signin
        """
        res = self.client().post(
            "/api/v1/auth/signup/",
            json=dict(firstname="John", lastname="Doe",
                      email="johndoe@email.com", username="@edwin",
                      is_admin=False, password="4747EdGr")
        )
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post(
            "/api/v1/auth/signin/",
            json=dict(email="johndoeemail.com", password="4747EdGr")
        )
        result = json.loads(second_res.data.decode())
        self.assertEqual(second_res.status_code, 400)
        self.assertEqual(
            str(result["message"]), "Invalid email. Valid format is example@email.com"
        )

    def tearDown(self):
        """
        Clean database
        """
        DB = Db()
        DB.delete_by_email("johndoe@email.com")

if __name__ == '__main__':
    unittest.main()
