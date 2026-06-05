from . import service_ticket_bp

@service_ticket_bp.route("/", methods=["GET"])
def get_service_tickets():
    return {"message": "Service ticket blueprint working"}