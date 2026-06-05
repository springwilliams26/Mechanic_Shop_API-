from flask import request, jsonify

from application.extensions import db
from application.models import (
    ServiceTicket,
    Customer,
    Mechanic,
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
    methods=["PUT"],
)
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
    methods=["PUT"],
)
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