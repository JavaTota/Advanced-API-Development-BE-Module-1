from flask import  request, jsonify
from marshmallow import ValidationError

from .schemas import inventory_schema, inventories_schema
from application.models import  Inventory, inventory, db
from . import inventory_bp
from application.extensions import limiter, cache


#========= Create ===========

@inventory_bp.route("/", methods=["POST"])
@limiter.limit("5 per day")
def create_inventory():
    try:
        inventory_data = inventory_schema.load(request.json)
        
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_inventory = Inventory(**inventory_data)
    db.session.add(new_inventory)
    db.session.commit()

    return inventory_schema.jsonify(new_inventory), 201

#========== Read ===========

@inventory_bp.route("/<int:inventory_id>", methods=["GET"])
@cache.cached(timeout=60)  # Cache this endpoint for 60 seconds
def get_inventory(inventory_id):
    try:
        inventory_data = db.session.get(Inventory, inventory_id)
        if not inventory_data:
            return jsonify({"error": "Part not found"}), 404
    except ValidationError as err:
        return jsonify(err.messages), 400

    return inventory_schema.jsonify(inventory_data), 200

@inventory_bp.route("/", methods=["GET"])
@cache.cached(timeout=60)  # Cache this endpoint for 60 seconds
def get_inventories():
    try:
        inventories_data = db.session.query(Inventory).all()
        
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    return inventories_schema.jsonify(inventories_data), 200        

#========== Update ===========

@inventory_bp.route("/<int:inventory_id>", methods=["PUT"])
def update_inventory(inventory_id):
    try:
        inventory_data = db.session.get(Inventory, inventory_id)
        if not inventory_data:
            return jsonify({"error": "Part not found"}), 404
        
        updated_data = inventory_schema.load(request.json, partial=True)
        
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    for key, value in updated_data.items():
        setattr(inventory_data, key, value)
    
    db.session.commit()

    return inventory_schema.jsonify(inventory_data), 200

#========== Delete ===========

@inventory_bp.route("/<int:inventory_id>", methods=["DELETE"])
def delete_inventory(inventory_id):
    inventory_data = db.session.get(Inventory, inventory_id)
    if not inventory_data:
        return jsonify({"error": "Part not found"}), 404

    db.session.delete(inventory_data)
    db.session.commit()

    return jsonify({"message": "Part deleted successfully"}), 200