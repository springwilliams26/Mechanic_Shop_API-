from flask import Flask
from config import Config
from application.extensions import db, ma

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)

    from application.blueprints.customer import customer_bp
    from application.blueprints.mechanic import mechanic_bp
    from application.blueprints.service_ticket import service_ticket_bp

    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")

    with app.app_context():
        from application import models
        db.create_all()

    return app