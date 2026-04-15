from flask import  request, jsonify
from marshmallow import ValidationError

from .schemas import costumer_schema, costumers_schema
from application.models import Costumer, db
from . import costumer_bp
from application.extensions import limiter

@costumer_bp.route("/", methods=["POST"])
@limiter.limit("5 per day")
def create_costumer():
    try:
        costumer_data = costumer_schema.load(request.json)
        
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_costumer = Costumer(**costumer_data)
    db.session.add(new_costumer)
    db.session.commit()

    return costumer_schema.jsonify(new_costumer), 201


#========== Read ===========


@costumer_bp.route("/<int:costumer_id>", methods=["GET"])
def get_costumer(costumer_id):
    try:
        costumer_data = db.session.get(Costumer, costumer_id)
        
    except ValidationError as err:
        return jsonify(err.messages), 400
     

    return costumer_schema.jsonify(costumer_data), 200


@costumer_bp.route("/", methods=["GET"])
def get_costumers():
    try:
        costumers_data = db.session.query(Costumer).all()
        
    except ValidationError as err:
        return jsonify(err.messages), 400
     

    return costumers_schema.jsonify(costumers_data), 200


#========== Update ===========


@costumer_bp.route("/<int:costumer_id>", methods=["PUT"])
@limiter.limit("5 per month")
def update_costumer(costumer_id):
    try:
        costumer_data = costumer_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    costumer = db.session.get(Costumer, costumer_id)
    if not costumer:
        return jsonify({"error": "Costumer not found"}), 404

    for key, value in costumer_data.items():
        setattr(costumer, key, value)

    db.session.commit()
    return costumer_schema.jsonify(costumer), 200


#========== Delete ===========


@costumer_bp.route("/<int:costumer_id>", methods=["DELETE"])
@limiter.limit("5 per year")
def delete_costumer(costumer_id):
    costumer = db.session.get(Costumer, costumer_id)
    if not costumer:
        return jsonify({"error": "Costumer not found"}), 404

    db.session.delete(costumer)
    db.session.commit()
    return jsonify({"message": "Costumer deleted"}), 200

