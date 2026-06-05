from flask import request, jsonify

from application.extensions import db
from application.models import (
    ServiceTicket,
    Customer,
    Mechanic,
    Inventory,
)

from . import service_ticket_bp
from .schemas import (
    service_ticket_schema,
    service_tickets_schema,
)


@service_ticket_bp.route("/", methods=["POST"])
def create_service_ticket():
    ticket_data = request.json

    customer = db.session.get(
        Customer,
        ticket_data["customer_id"],
    )

    if not customer:
        return jsonify(
            {"error": "Customer not found."}
        ), 404

    new_ticket = ServiceTicket(
        description=ticket_data["description"],
        vin=ticket_data["vin"],
        service_date=ticket_data["service_date"],
        customer_id=ticket_data["customer_id"],
    )

    db.session.add(new_ticket)
    db.session.commit()

    return service_ticket_schema.jsonify(
        new_ticket
    ), 201


@service_ticket_bp.route("/", methods=["GET"])
def get_service_tickets():
    tickets = ServiceTicket.query.all()

    return service_tickets_schema.jsonify(
        tickets
    ), 200


@service_ticket_bp.route(
    "/<int:ticket_id>/assign-mechanic/<int:mechanic_id>",
    methods=["PUT"],)
def assign_mechanic(ticket_id, mechanic_id):

    ticket = db.session.get(
        ServiceTicket,
        ticket_id,
    )

    mechanic = db.session.get(
        Mechanic,
        mechanic_id,
    )

    if not ticket:
        return jsonify(
            {"error": "Ticket not found."}
        ), 404

    if not mechanic:
        return jsonify(
            {"error": "Mechanic not found."}
        ), 404

    ticket.mechanics.append(mechanic)

    db.session.commit()

    return jsonify(
        {"message": "Mechanic assigned."}
    ), 200


@service_ticket_bp.route(
    "/<int:ticket_id>/remove-mechanic/<int:mechanic_id>",
    methods=["PUT"],)
def remove_mechanic(ticket_id, mechanic_id):

    ticket = db.session.get(
        ServiceTicket,
        ticket_id,
    )

    mechanic = db.session.get(
        Mechanic,
        mechanic_id,
    )

    if not ticket:
        return jsonify(
            {"error": "Ticket not found."}
        ), 404

    if not mechanic:
        return jsonify(
            {"error": "Mechanic not found."}
        ), 404

    ticket.mechanics.remove(mechanic)

    db.session.commit()

    return jsonify(
        {"message": "Mechanic removed."}
    ), 200
    
    
@service_ticket_bp.route("/<int:ticket_id>/edit", methods=["PUT"])
def edit_ticket_mechanics(ticket_id):

    ticket = db.session.get(ServiceTicket, ticket_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    data = request.json

    add_ids = data.get("add_ids", [])
    remove_ids = data.get("remove_ids", [])

    for mechanic_id in add_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)

        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)

    for mechanic_id in remove_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)

        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)

    db.session.commit()

    return jsonify(
        {"message": "Service ticket mechanics updated successfully."}
    ), 200
    
@service_ticket_bp.route(
    "/<int:ticket_id>/add-part/<int:part_id>",
    methods=["PUT"],)
def add_part_to_ticket(ticket_id, part_id):

    ticket = db.session.get(ServiceTicket, ticket_id)

    part = db.session.get(Inventory, part_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    if not part:
        return jsonify({"error": "Inventory item not found."}), 404

    if part not in ticket.parts:
        ticket.parts.append(part)

    db.session.commit()

    return jsonify(
        {"message": "Inventory item added to service ticket successfully."}
    ), 200