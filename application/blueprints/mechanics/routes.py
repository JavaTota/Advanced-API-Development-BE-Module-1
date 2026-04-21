from flask import  request, jsonify
from marshmallow import ValidationError

from .schemas import mechanic_schema, mechanics_schema
from application.models import  Mechanic, db
from . import mechanic_bp
from application.extensions import limiter, cache

@mechanic_bp.route("/", methods=["POST"])
@limiter.limit("5 per day")
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
        
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()

    return mechanic_schema.jsonify(new_mechanic), 201


#========== Read ===========


@mechanic_bp.route("/<int:mechanic_id>", methods=["GET"])
@cache.cached(timeout=60)  # Cache this endpoint for 60 seconds
def get_mechanic(mechanic_id):
    try:
        mechanic_data = db.session.get(Mechanic, mechanic_id)
        
    except ValidationError as err:
        return jsonify(err.messages), 400
     

    return mechanic_schema.jsonify(mechanic_data), 200


@mechanic_bp.route("/", methods=["GET"])
@cache.cached(timeout=60)  # Cache this endpoint for 60 seconds
def get_mechanics():
    try:
        mechanics_data = db.session.query(Mechanic).all()
        
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    

    return mechanics_schema.jsonify(mechanics_data), 200

#========= Get Popular Mechanics(sorting) ===========

@mechanic_bp.route("/popular", methods=["GET"])
@cache.cached(timeout=60)  # Cache this endpoint for 60 seconds
def get_popular_mechanics():
    
    mechanics_data = db.session.query(Mechanic).all()
    
    # Sort mechanics by the number of service tickets they are assigned to, in descending order
    mechanics_data.sort(key=lambda m: len(m.service_tickets), reverse=True)

    

    return mechanics_schema.jsonify(mechanics_data), 200


#========== Update ===========


@mechanic_bp.route("/<int:mechanic_id>", methods=["PUT"])
@limiter.limit("5 per month")
def update_mechanic(mechanic_id):
    try:
        mechanic_data = mechanic_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


#========== Delete ===========


@mechanic_bp.route("/<int:mechanic_id>", methods=["DELETE"])
@limiter.limit("5 per year")
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic deleted"}), 200

#========== Search Mechanics ===========

@mechanic_bp.route("/search", methods=["GET"])
def search_mechanics():
    name_query = request.args.get("name")
    if not name_query:
        return jsonify({"error": "Name query parameter is required"}), 400

    mechanics_data = db.session.query(Mechanic).where(Mechanic.name.like(f"%{name_query}%")).all()
    
    return mechanics_schema.jsonify(mechanics_data), 200