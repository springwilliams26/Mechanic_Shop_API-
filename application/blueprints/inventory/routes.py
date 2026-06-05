from flask import request, jsonify
from marshmallow import ValidationError

from application.extensions import db
from application.models import Inventory
from . import inventory_bp
from .schemas import inventory_schema, inventory_items_schema


@inventory_bp.route("/", methods=["POST"])
def create_inventory_item():
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_item = Inventory(**inventory_data)

    db.session.add(new_item)
    db.session.commit()

    return inventory_schema.jsonify(new_item), 201


@inventory_bp.route("/", methods=["GET"])
def get_inventory_items():
    inventory_items = Inventory.query.all()

    return inventory_items_schema.jsonify(inventory_items), 200


@inventory_bp.route("/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)

    if not item:
        return jsonify({"error": "Inventory item not found."}), 404

    return inventory_schema.jsonify(item), 200


@inventory_bp.route("/<int:item_id>", methods=["PUT"])
def update_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)

    if not item:
        return jsonify({"error": "Inventory item not found."}), 404

    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in inventory_data.items():
        setattr(item, key, value)

    db.session.commit()

    return inventory_schema.jsonify(item), 200


@inventory_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)

    if not item:
        return jsonify({"error": "Inventory item not found."}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify(
        {"message": f"Inventory item {item_id} deleted successfully."}
    ), 200