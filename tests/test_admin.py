"""
Tests for admin endpoints
"""
import unittest
import json
from app import create_app
from models.db import Db

class AdminTestCases(unittest.TestCase):
    """
    Class for admin tests cases
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

    def login_admin(self, email="admin@admin.com", password="adminEdGr17"):
        """
        Helper function to login user
        """
        return self.client().post("/api/v1/auth/signin/",
                                  json=dict(email=email, password=password)
                                 )

    def test_unauthorized_access(self):
        """
        Test API can handle unauthorized access
        """
        self.register_user()
        user = self.login_user()
        user_token = json.loads(user.data.decode())["token"]

        res = self.client().get(
            "/api/v1/requests/",
            headers=dict(Authorization="Bearer " + user_token)
        )
        self.assertEqual(res.status_code, 401)
        result = json.loads(res.data.decode())
        self.assertEqual(result["message"], "You don't have the right access to access this view")


    def test_unauthorized_approve_access(self):
        """
        Test API can handle unauthorized approve access
        """
        self.register_user()
        user = self.login_user()
        user_token = json.loads(user.data.decode())["token"]

        res = self.client().put(
            "/api/v1/requests/1/approve/",
            headers=dict(Authorization="Bearer " + user_token),
            json=dict(approved="true")
        )
        self.assertEqual(res.status_code, 401)
        result = json.loads(res.data.decode())
        self.assertEqual(result["message"], "You don't have the right access to approve this request.")

    def test_unauthorized_reject_access(self):
        """
        Test API can handle unauthorized reject access
        """
        self.register_user()
        user = self.login_user()
        user_token = json.loads(user.data.decode())["token"]

        res = self.client().put(
            "/api/v1/requests/1/reject/",
            headers=dict(Authorization="Bearer " + user_token),
            json=dict(rejected="true")
        )
        self.assertEqual(res.status_code, 401)
        result = json.loads(res.data.decode())
        self.assertEqual(result["message"], "You don't have the right access to reject this request.")

    def test_unauthorized_resolve_access(self):
        """
        Test API can handle unauthorized resolve access
        """
        self.register_user()
        user = self.login_user()
        user_token = json.loads(user.data.decode())["token"]

        res = self.client().put(
            "/api/v1/requests/1/resolve/",
            headers=dict(Authorization="Bearer " + user_token),
            json=dict(resolved="true")
        )
        self.assertEqual(res.status_code, 401)
        result = json.loads(res.data.decode())
        self.assertEqual(result["message"], "You don't have the right access to resolve this request.")

    def test_unauthorized_approve_privilege(self):
        """
        Test API can handle unauthorized approve access
        """
        admin = self.login_admin()
        admin_token = json.loads(admin.data.decode())["token"]

        res = self.client().put(
            "/api/v1/requests/1/approve/",
            headers=dict(Authorization="Bearer " + admin_token),
            json=dict(resolved="true")
        )
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result["message"], "You only need to approve a request.")

    def test_unauthorized_reject_privilege(self):
        """
        Test API can handle unauthorized reject access
        """
        admin = self.login_admin()
        admin_token = json.loads(admin.data.decode())["token"]

        res = self.client().put(
            "/api/v1/requests/1/reject/",
            headers=dict(Authorization="Bearer " + admin_token),
            json=dict(approved="true")
        )
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result["message"], "You only need to reject a request.")

    def test_unauthorized_approve_request_access(self):
        """
        Test API can handle unauthorized approve edit access
        """
        self.register_user()
        user = self.login_user()
        user_token = json.loads(user.data.decode())["token"]

        res = self.client().put(
            "/api/v1/requests/1/approve/",
            headers=dict(Authorization="Bearer " + user_token),
            json=dict(approved="true")
        )
        self.assertEqual(res.status_code, 401)
        result = json.loads(res.data.decode())
        self.assertEqual(result["message"], "You don't have the right access to approve this request.")

    def test_unauthorized_reject_request_access(self):
        """
        Test API can handle unauthorized reject edit access
        """
        self.register_user()
        user = self.login_user()
        user_token = json.loads(user.data.decode())["token"]

        res = self.client().put(
            "/api/v1/requests/1/reject/",
            headers=dict(Authorization="Bearer " + user_token),
            json=dict(rejected="true")
        )
        self.assertEqual(res.status_code, 401)
        result = json.loads(res.data.decode())
        self.assertEqual(result["message"], "You don't have the right access to reject this request.")

    def test_unauthorized_resolve_request_access(self):
        """
        Test API can handle unauthorized resolve edit access
        """
        self.register_user()
        user = self.login_user()
        user_token = json.loads(user.data.decode())["token"]

        res = self.client().put(
            "/api/v1/requests/1/resolve/",
            headers=dict(Authorization="Bearer " + user_token),
            json=dict(resolved="true")
        )
        self.assertEqual(res.status_code, 401)
        result = json.loads(res.data.decode())
        self.assertEqual(result["message"], "You don't have the right access to resolve this request.")




    def test_unauthorized_resolve_privilege(self):
        """
        Test API can handle unauthorized resolve access
        """
        admin = self.login_admin()
        admin_token = json.loads(admin.data.decode())["token"]

        res = self.client().put(
            "/api/v1/requests/1/resolve/",
            headers=dict(Authorization="Bearer " + admin_token),
            json=dict(rejected="true")
        )
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result["message"], "You only need to resolve a request.")

    def tearDown(self):
        """
        Clean up database
        """
        DB = Db()
        DB.delete_by_email("johndoe@gmail.com")

if __name__ == '__main__':
    unittest.main()
