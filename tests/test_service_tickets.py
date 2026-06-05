import unittest

from application import create_app
from application.extensions import db
from application.models import (
    Customer,
    Mechanic,
    ServiceTicket,
    Inventory,
)
from config import TestingConfig


class TestServiceTickets(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            self.customer = Customer(
                name="Customer",
                email="customer@test.com",
                phone="555-111-1111",
                address="Test Address",
                password="password123",
            )

            self.mechanic = Mechanic(
                name="Mechanic",
                email="mechanic@test.com",
                phone="555-222-2222",
                salary=65000,
            )

            self.inventory = Inventory(
                name="Brake Pads",
                price=89.99,
            )

            db.session.add(self.customer)
            db.session.add(self.mechanic)
            db.session.add(self.inventory)
            db.session.commit()

            self.ticket = ServiceTicket(
                description="Brake Repair",
                vin="VIN123456",
                service_date="2026-06-06",
                customer_id=self.customer.id,
            )

            db.session.add(self.ticket)
            db.session.commit()

    def test_create_service_ticket(self):
        payload = {
            "description": "Oil Change",
            "vin": "VIN999999",
            "service_date": "2026-06-07",
            "customer_id": 1,
        }

        response = self.client.post(
            "/service-tickets/",
            json=payload,
        )

        self.assertEqual(response.status_code, 201)

    def test_create_service_ticket_invalid_customer(self):
        payload = {
            "description": "Oil Change",
            "vin": "VIN999999",
            "service_date": "2026-06-07",
            "customer_id": 999,
        }

        response = self.client.post(
            "/service-tickets/",
            json=payload,
        )

        self.assertEqual(response.status_code, 404)

    def test_get_service_tickets(self):
        response = self.client.get("/service-tickets/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_assign_mechanic(self):
        response = self.client.put(
            "/service-tickets/1/assign-mechanic/1"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["message"],
            "Mechanic assigned.",
        )

    def test_assign_mechanic_invalid_ticket(self):
        response = self.client.put(
            "/service-tickets/999/assign-mechanic/1"
        )

        self.assertEqual(response.status_code, 404)

    def test_remove_mechanic(self):

        self.client.put(
            "/service-tickets/1/assign-mechanic/1"
        )

        response = self.client.put(
            "/service-tickets/1/remove-mechanic/1"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["message"],
            "Mechanic removed.",
        )

    def test_edit_ticket_mechanics(self):

        payload = {
            "add_ids": [1],
            "remove_ids": [],
        }

        response = self.client.put(
            "/service-tickets/1/edit",
            json=payload,
        )

        self.assertEqual(response.status_code, 200)

    def test_add_part_to_ticket(self):

        response = self.client.put(
            "/service-tickets/1/add-part/1"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["message"],
            "Inventory item added to service ticket successfully.",
        )

    def test_add_part_invalid_ticket(self):

        response = self.client.put(
            "/service-tickets/999/add-part/1"
        )

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()