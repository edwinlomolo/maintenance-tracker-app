"""
Tests for user
 ==> Signup
 ==> SignIn
 ==> Invalid credentials
 ==> Token generation
 ===> Token validation
"""
import os
import psycopg2
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

    def test_account_duplication(self):
        """
        Test API can handle email duplication error
        """
        res = self.client().post(
            "/api/v1.0/auth/signup/",
            json=dict(email="johndoe@email.com", password="4747")
        )
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 202)
        self.assertEqual(
            str(result["message"]), "Email already taken. Please choose a different one."
        )

    def test_signup_input(self):
        """
        Test API can handle empty requests during signup
        """
        res = self.client().post("/api/v1.0/auth/signup/")
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(result["error"]), "Please provide both an email and a password.")

    def test_email_signup(self):
        """
        Test API can handle orphaned email input during signup
        """
        res = self.client().post(
            "/api/v1.0/auth/signup/",
            json=dict(email="johndoe@email.com")
        )
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            str(result["error"]), "Please provide both an email and a password."
        )

    def test_password_signup(self):
        """
        Test API can handle orphaned password input during signup
        """
        res = self.client().post(
            "/api/v1.0/auth/signup/",
            json=dict(password="4747")
        )
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 202)
        self.assertEqual(
            str(result["error"]), "Please provide both an email and a password."
        )

    def test_user_can_log_in(self):
        """
        Test API can authenticate user
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
        self.assertIn("eY", str(result["token"]))

    def test_unauthorized_access(self):
        """
        Test API can handle unauthorized access
        """

        res = self.client().post(
            "/api/v1.0/auth/signin/",
            json=dict(email="johndoe@email.com", password="474")
        )
        result = json.loads(res.data.decode())
        res = self.client().post("/users/api/v1.0/authenticate/", json=dict(
            email="milly@gmail.com",
            password=12
        ))
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 401)
        self.assertEqual(result["error"], "Invalid password or email.")

    def test_signin_input(self):
        """
        Test API can handle empty requests during signin
        """
        res = self.client().post("/api/v1.0/auth/signin/")
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(result["error"]), "Invalid email or password.")

    def test_orphaned_email(self):
        """
        Test API can handle orphaned email input during signin
        """
        res = self.client().post(
            "/api/v1.0/auth/signin/",
            json=dict(email="johndoe@email.com")
        )
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            str(result["error"]), "Invalid email or password."
        )

    def test_orphaned_password(self):
        """
        Test API can handle orphaned password input
        """
        res = self.client().post(
            "/api/v1.0/auth/signup/",
            json=dict(password="4747")
        )
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 202)
        self.assertEqual(
            str(result["error"]), "Invalid email or password."
        )

    def test_api_can_handle_empty_response(self):
      """
      Test API can handle empty or invalid request
      """
        res = self.client().post("/users/api/v1.0/account/register/")
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(data["error"]), "Bad request")
     def tearDown(self):
        """
        Clean up database after running tests
        """
        conn = None
        try:
            conn = psycopg2.connect(
                host=os.getenv("HOST"),
                database=os.getenv("DATABASE"),
                user=os.getenv("USER"),
                password=os.getenv("PASS")
            )

            query = """DELETE FROM USERS WHERE EMAIL = %s"""
            email = "johndoe@email.com"

            cur = conn.cursor()
            cur.execute(query, (email,))

            cur.close()
            conn.commit()
        except(Exception, psycopg2.DatabaseError) as error: # pylint: disable=broad-except
            print error
        finally:
            if conn is not None:
                conn.close()

if __name__ == '__main__':
    unittest.main()
