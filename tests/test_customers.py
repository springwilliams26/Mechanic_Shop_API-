import unittest

from application import create_app
from application.extensions import db
from application.models import Customer
from config import TestingConfig


class TestCustomers(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            customer = Customer(
                name="Test Customer",
                email="test@example.com",
                phone="555-123-4567",
                address="123 Test Street",
                password="password123",
            )

            db.session.add(customer)
            db.session.commit()

    def test_create_customer(self):
        payload = {
            "name": "Spring Williams",
            "email": "spring@example.com",
            "phone": "555-999-8888",
            "address": "456 Main Street",
            "password": "password123",
        }

        response = self.client.post("/customers/", json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["email"], "spring@example.com")

    def test_create_customer_duplicate_email(self):
        payload = {
            "name": "Duplicate Customer",
            "email": "test@example.com",
            "phone": "555-000-0000",
            "address": "Duplicate Street",
            "password": "password123",
        }

        response = self.client.post("/customers/", json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Email already exists.")

    def test_get_customers(self):
        response = self.client.get("/customers/?page=1&per_page=5")

        self.assertEqual(response.status_code, 200)
        self.assertIn("customers", response.json)
        self.assertEqual(response.json["total"], 1)

    def test_update_customer(self):
        payload = {
            "name": "Updated Customer",
            "email": "updated@example.com",
            "phone": "555-222-3333",
            "address": "Updated Address",
            "password": "newpassword",
        }

        response = self.client.put("/customers/1", json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Updated Customer")

    def test_delete_customer(self):
        response = self.client.delete("/customers/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["message"],
            "Customer 1 deleted successfully.",
        )

    def test_login_customer(self):
        payload = {
            "email": "test@example.com",
            "password": "password123",
        }

        response = self.client.post("/customers/login", json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        self.assertIn("auth_token", response.json)

    def test_invalid_login(self):
        payload = {
            "email": "bad@example.com",
            "password": "wrongpassword",
        }

        response = self.client.post("/customers/login", json=payload)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json["message"], "Invalid email or password.")

    def test_my_tickets_requires_token(self):
        response = self.client.get("/customers/my-tickets")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json["message"], "Token is missing.")


if __name__ == "__main__":
    unittest.main()