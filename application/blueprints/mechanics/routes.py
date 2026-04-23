from sqlalchemy import select
from flask import  request, jsonify
from marshmallow import ValidationError

from application.utils.util import encode_token, token_required

from .schemas import mechanic_schema, mechanics_schema, login_schema
from application.models import  Mechanic, db
from . import mechanic_bp
from application.extensions import limiter, cache


#========== Authentication ===========

@mechanic_bp.route("/login", methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)# we use the login schema to validate the incoming data, which only requires email and password fields
        email = credentials['email']
        password = credentials['password']
        
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    query = select(Mechanic).where(Mechanic.email == email) 
    mechanic = db.session.execute(query).scalars().first() #Query mechanic table for a mechanic with this email

    if mechanic and mechanic.password == password: #if we have a mechanic associated with the email and the password is correct, validate the password
        auth_token = encode_token(mechanic.id, "mechanic") #generate an auth token with the mechanic's id as the payload

        response = {
            "status": "success",
            "message": "Successfully Logged In",
            "auth_token": auth_token
        }
        return jsonify(response), 200
    else:
        return jsonify({'messages': "Invalid email or password"}), 401

#========= Create ===========

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
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)

        query = db.select(Mechanic)
        paginated_mechanics = db.paginate(query, page=page, per_page=per_page)

        if not paginated_mechanics.items:
            return jsonify({"message": "No mechanics found"}), 404

    except ValidationError as err:
        return jsonify(err.messages), 400
    

    

    return mechanics_schema.jsonify(paginated_mechanics), 200

#========= Get Popular Mechanics(sorting) ===========

@mechanic_bp.route("/popular", methods=["GET"])
@cache.cached(timeout=60)  # Cache this endpoint for 60 seconds
def get_popular_mechanics():
    
    mechanics_data = db.session.query(Mechanic).all()
    
    # Sort mechanics by the number of service tickets they are assigned to, in descending order
    mechanics_data.sort(key=lambda m: len(m.service_tickets), reverse=True)

    

    return mechanics_schema.jsonify(mechanics_data), 200


#========== Update ===========


@mechanic_bp.route("/", methods=["PUT"])
@limiter.limit("5 per month")
@token_required
def update_mechanic(current_id, current_role):
    try:
        mechanic_data = mechanic_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    mechanic = db.session.get(Mechanic, current_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    if current_role != "mechanic":
        return jsonify({"error": "Unauthorized"}), 403

    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


#========== Delete ===========


@mechanic_bp.route("/", methods=["DELETE"])
# @limiter.limit("5 per year")
@token_required
def delete_mechanic(current_id, current_role):
    query = select(Mechanic).where(Mechanic.id == current_id)
    mechanic = db.session.execute(query).scalars().first()
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    if current_role != "mechanic":
        return jsonify({"error": "Unauthorized"}), 403

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