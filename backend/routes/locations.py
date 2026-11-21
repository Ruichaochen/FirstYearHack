from flask import Blueprint, jsonify, request
from database import db
from models.location import Location, Production, LocationProduction, ProductionInfo

locations_bp = Blueprint("locations", __name__)


@locations_bp.route("/api/locations", methods=["GET"])
def get_locations():
    """Get all locations, optionally filtered by category and/or search query."""
    category = request.args.get("category")
    search = request.args.get("search")

    if search:
        # Search by location name OR associated production name (case-insensitive)
        search_pattern = f"%{search}%"
        location_ids_with_matching_production = db.session.query(LocationProduction.location_id).join(
            Production
        ).filter(Production.name.ilike(search_pattern)).distinct()

        query = Location.query.filter(
            db.or_(
                Location.name.ilike(search_pattern),
                Location.id.in_(location_ids_with_matching_production)
            )
        )

        if category:
            query = query.filter_by(category=category)
    elif category:
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
