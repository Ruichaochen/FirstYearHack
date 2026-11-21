from flask import Blueprint, jsonify, request
from models.location import Location

locations_bp = Blueprint("locations", __name__)


@locations_bp.route("/api/locations", methods=["GET"])
def get_locations():
    """Get all locations, optionally filtered by category."""
    category = request.args.get("category")

    if category:
        query = Location.query.filter_by(category=category)
    else:
        query = Location.query

    locations = query.all()
    return jsonify([loc.to_dict() for loc in locations])


@locations_bp.route("/api/locations/<int:location_id>", methods=["GET"])
def get_location(location_id):
    """Get a single location by ID."""
    location = Location.query.get(location_id)

    if location is None:
        return jsonify({"error": "Location not found"}), 404

    return jsonify(location.to_dict())


@locations_bp.route("/api/categories", methods=["GET"])
def get_categories():
    """Get all available categories."""
    categories = Location.query.with_entities(Location.category).distinct().all()
    category_list = [c[0] for c in categories]
    return jsonify(category_list)
