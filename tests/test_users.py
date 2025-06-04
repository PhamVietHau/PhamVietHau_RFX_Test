# Test user-related functionality
import unittest

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class Test_User(unittest.TestCase):

    # Create user
    def test_create_user(self):
        response = client.post(
            "/users", json={"name": "Nguyen Van Ks", "email": "ks@gmail.com"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["email"], "ks@gmail.com")

    # Get user by id
    def test_get_user_by_id(self):
        create = client.post(
            "/users", json={"name": "Nguyen Van Sq", "email": "sq@gmail.com"}
        )
        create_resp = create.json()
        response = client.get(f"/users/{create_resp["id"]}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], create_resp["id"])
        self.assertEqual(data["name"], create_resp["name"])
        self.assertEqual(data["email"], create_resp["email"])

    # List user
    def test_list_users(self):
        response = client.get("/users")
        self.assertEqual(response.status_code, 200)
