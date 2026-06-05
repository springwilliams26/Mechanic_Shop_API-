from . import mechanic_bp

@mechanic_bp.route("/", methods=["GET"])
def get_mechanics():
    return {"message": "Mechanic blueprint working"}