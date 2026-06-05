from flask import Flask, app
from config import Config
from application.extensions import db, ma, limiter, cache

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    from application.blueprints.customer import customer_bp
    from application.blueprints.mechanic import mechanic_bp
    from application.blueprints.service_ticket import service_ticket_bp
    from application.blueprints.inventory import inventory_bp

    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    with app.app_context():
        from application import models
        db.create_all()

    return app