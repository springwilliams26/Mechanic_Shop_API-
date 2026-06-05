import unittest

from application import create_app
from application.extensions import db
from application.models import Mechanic, ServiceTicket, Customer
from config import TestingConfig


class TestMechanics(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            self.customer = Customer(
                name="Test Customer",
                email="customer@example.com",
                phone="555-123-4567",
                address="123 Test Street",
                password="password123",
            )

            self.mechanic = Mechanic(
                name="Test Mechanic",
                email="mechanic@example.com",
                phone="555-111-2222",
                salary=65000,
            )

            self.ticket = ServiceTicket(
                description="Brake repair",
                vin="1HGCM82633A123456",
                service_date="2026-06-06",
                customer_id=1,
            )

            db.session.add(self.customer)
            db.session.add(self.mechanic)
            db.session.commit()

            db.session.add(self.ticket)
            db.session.commit()

            self.ticket.mechanics.append(self.mechanic)
            db.session.commit()

    def test_create_mechanic(self):
        payload = {
            "name": "New Mechanic",
            "email": "newmechanic@example.com",
            "phone": "555-999-8888",
            "salary": 70000,
        }

        response = self.client.post("/mechanics/", json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["email"], "newmechanic@example.com")

    def test_create_mechanic_duplicate_email(self):
        payload = {
            "name": "Duplicate Mechanic",
            "email": "mechanic@example.com",
            "phone": "555-000-0000",
            "salary": 60000,
        }

        response = self.client.post("/mechanics/", json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Email already exists.")

    def test_get_mechanics(self):
        response = self.client.get("/mechanics/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_get_mechanic_by_id(self):
        response = self.client.get("/mechanics/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Test Mechanic")

    def test_get_mechanic_not_found(self):
        response = self.client.get("/mechanics/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Mechanic not found.")

    def test_update_mechanic(self):
        payload = {
            "name": "Updated Mechanic",
            "email": "updatedmechanic@example.com",
            "phone": "555-222-3333",
            "salary": 75000,
        }

        response = self.client.put("/mechanics/1", json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Updated Mechanic")

    def test_delete_mechanic(self):
        response = self.client.delete("/mechanics/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["message"],
            "Mechanic 1 deleted successfully.",
        )

    def test_top_mechanics(self):
        response = self.client.get("/mechanics/top-mechanics")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]["name"], "Test Mechanic")
        self.assertEqual(response.json[0]["tickets_completed"], 1)


if __name__ == "__main__":
    unittest.main()