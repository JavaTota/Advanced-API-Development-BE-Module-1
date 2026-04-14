from flask import  request, jsonify
from marshmallow import ValidationError

from .schemas import mechanic_schema, mechanics_schema
from application.models import  Mechanic, db
from . import mechanic_bp

@mechanic_bp.route("/", methods=["POST"])
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
def get_mechanic(mechanic_id):
    try:
        mechanic_data = db.session.get(Mechanic, mechanic_id)
        
    except ValidationError as err:
        return jsonify(err.messages), 400
     

    return mechanic_schema.jsonify(mechanic_data), 200


@mechanic_bp.route("/", methods=["GET"])
def get_mechanics():
    try:
        mechanics_data = db.session.query(Mechanic).all()
        
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    

    return mechanics_schema.jsonify(mechanics_data), 200




#========== Update ===========


@mechanic_bp.route("/<int:mechanic_id>", methods=["PUT"])
def update_mechanic(mechanic_id):
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    mechanic.name = mechanic_data.get("name", mechanic.name)
    mechanic.email = mechanic_data.get("email", mechanic.email)
    mechanic.phone = mechanic_data.get("phone", mechanic.phone)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


#========== Delete ===========


@mechanic_bp.route("/<int:mechanic_id>", methods=["DELETE"])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic deleted"}), 200

