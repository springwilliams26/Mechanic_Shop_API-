from flask import request, jsonify
from marshmallow import ValidationError
from application.extensions import db, limiter, cache
from . import customer_bp
from application.models import Customer, ServiceTicket
from .schemas import customer_schema, customers_schema, login_schema
from application.utils.util import encode_token, token_required

@customer_bp.route("/", methods=["POST"])
@limiter.limit("5 per minute")
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    existing_customer = Customer.query.filter_by(
        email=customer_data["email"]
    ).first()

    if existing_customer:
        return jsonify({"error": "Email already exists."}), 400

    new_customer = Customer(**customer_data)

    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201


@customer_bp.route("/", methods=["GET"])
@cache.cached(timeout=60)
def get_customers():

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    customers = Customer.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False,
    )

    return jsonify(
        {
            "customers": customers_schema.dump(customers.items),
            "total": customers.total,
            "pages": customers.pages,
            "current_page": customers.page,
        }
    ), 200


@customer_bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in customer_data.items():
        setattr(customer, key, value)

    db.session.commit()

    return customer_schema.jsonify(customer), 200


@customer_bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify(
        {"message": f"Customer {customer_id} deleted successfully."}
    ), 200
    
    
@customer_bp.route("/login", methods=["POST"])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials["email"]
        password = credentials["password"]

    except KeyError:
        return jsonify(
            {"message": "Invalid payload. Email and password are required."}
        ), 400

    except ValidationError as e:
        return jsonify(e.messages), 400

    customer = Customer.query.filter_by(email=email).first()

    if customer and customer.password == password:
        auth_token = encode_token(customer.id)

        return jsonify(
            {
                "status": "success",
                "message": "Successfully logged in.",
                "auth_token": auth_token,
            }
        ), 200

    return jsonify({"message": "Invalid email or password."}), 401


@customer_bp.route("/my-tickets", methods=["GET"])
@token_required
def get_my_tickets(customer_id):
    tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()

    return jsonify(
        [
            {
                "id": ticket.id,
                "description": ticket.description,
                "vin": ticket.vin,
                "service_date": ticket.service_date,
                "customer_id": ticket.customer_id,
            }
            for ticket in tickets
        ]
    ), 200   