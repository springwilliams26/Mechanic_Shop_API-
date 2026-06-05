from application.extensions import db

# Many-to-Many Junction Table
service_mechanics = db.Table(
    "service_mechanics",
    db.Column(
        "service_ticket_id",
        db.Integer,
        db.ForeignKey("service_ticket.id"),
        primary_key=True,
    ),
    db.Column(
        "mechanic_id",
        db.Integer,
        db.ForeignKey("mechanic.id"),
        primary_key=True,
    ),
)


class Customer(db.Model):
    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    phone = db.Column(db.String(20))

    address = db.Column(db.String(200))

    password = db.Column(db.String(255), nullable=False)

    service_tickets = db.relationship(
        "ServiceTicket",
        back_populates="customer",
        cascade="all, delete-orphan",
    )


class Mechanic(db.Model):
    __tablename__ = "mechanic"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True)

    phone = db.Column(db.String(20))

    salary = db.Column(db.Float)

    service_tickets = db.relationship(
        "ServiceTicket",
        secondary=service_mechanics,
        back_populates="mechanics",
    )


class ServiceTicket(db.Model):
    __tablename__ = "service_ticket"

    id = db.Column(db.Integer, primary_key=True)

    description = db.Column(db.String(500))

    vin = db.Column(db.String(50))

    service_date = db.Column(db.String(50))

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customer.id"),
        nullable=False,
    )

    customer = db.relationship(
        "Customer",
        back_populates="service_tickets",
    )

    mechanics = db.relationship(
        "Mechanic",
        secondary=service_mechanics,
        back_populates="service_tickets",
    )