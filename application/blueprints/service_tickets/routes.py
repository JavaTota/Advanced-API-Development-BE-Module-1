from flask import  request, jsonify
from marshmallow import ValidationError

from .schemas import service_ticket_schema, service_tickets_schema
from application.models import ServiceTicket, Mechanic, db
from . import service_ticket_bp
from application.extensions import limiter

@service_ticket_bp.route("/", methods=["POST"])
@limiter.limit("5 per day")
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
        
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_service_ticket = ServiceTicket(**service_ticket_data)
    db.session.add(new_service_ticket)
    db.session.commit()

    return service_ticket_schema.jsonify(new_service_ticket), 201


#========== Read ===========


@service_ticket_bp.route("/<int:service_ticket_id>", methods=["GET"])
def get_service_ticket(service_ticket_id):
    try:
        service_ticket_data = db.session.get(ServiceTicket, service_ticket_id)
        
    except ValidationError as err:
        return jsonify(err.messages), 400
     

    return service_ticket_schema.jsonify(service_ticket_data), 200


@service_ticket_bp.route("/", methods=["GET"])
def get_service_tickets():
    try:
        service_tickets_data = db.session.query(ServiceTicket).all()
        
    except ValidationError as err:
        return jsonify(err.messages), 400
     

    return service_tickets_schema.jsonify(service_tickets_data), 200


#========== Update ===========


@service_ticket_bp.route("/<int:service_ticket_id>/assign_mechanic/<int:mechanic_id>", methods=["PUT"])
@limiter.limit("5 per month")
def assign_mechanic_to_service_ticket(service_ticket_id, mechanic_id):

    service_ticket = db.session.get(ServiceTicket, service_ticket_id)
    if not service_ticket:
        return jsonify({"error": "service_ticket not found"}), 404
    
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "mechanic not found"}), 404
    
    service_ticket.mechanics.append(mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200

@service_ticket_bp.route("/<int:service_ticket_id>/remove_mechanic/<int:mechanic_id>", methods=["PUT"])
@limiter.limit("5 per month")
def remove_mechanic_from_service_ticket(service_ticket_id, mechanic_id):

    service_ticket = db.session.get(ServiceTicket, service_ticket_id)
    if not service_ticket:
        return jsonify({"error": "service_ticket not found"}), 404
    
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "mechanic not found"}), 404
    
    service_ticket.mechanics.remove(mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200

#========== Delete ===========


@service_ticket_bp.route("/<int:service_ticket_id>", methods=["DELETE"])
@limiter.limit("5 per year")
def delete_service_ticket(service_ticket_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)
    if not service_ticket:
        return jsonify({"error": "service_ticket not found"}), 404

    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"message": "service_ticket deleted"}), 200

