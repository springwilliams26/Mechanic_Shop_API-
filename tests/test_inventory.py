import unittest

from application import create_app
from application.extensions import db
from application.models import Inventory
from config import TestingConfig


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            item = Inventory(
                name="Brake Pads",
                price=89.99,
            )

            db.session.add(item)
            db.session.commit()

    def test_create_inventory_item(self):
        payload = {
            "name": "Oil Filter",
            "price": 19.99,
        }

        response = self.client.post("/inventory/", json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "Oil Filter")

    def test_get_inventory_items(self):
        response = self.client.get("/inventory/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_get_inventory_item_by_id(self):
        response = self.client.get("/inventory/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Brake Pads")

    def test_get_inventory_item_not_found(self):
        response = self.client.get("/inventory/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Inventory item not found.")

    def test_update_inventory_item(self):
        payload = {
            "name": "Updated Brake Pads",
            "price": 99.99,
        }

        response = self.client.put("/inventory/1", json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Updated Brake Pads")

    def test_delete_inventory_item(self):
        response = self.client.delete("/inventory/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["message"],
            "Inventory item 1 deleted successfully.",
        )


if __name__ == "__main__":
    unittest.main()