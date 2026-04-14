from flask import  request, jsonify
from marshmallow import ValidationError

from .schemas import service_ticket_schema, service_tickets_schema
from application.models import ServiceTickets, db
from . import service_ticket_bp

@service_ticket_bp.route("/", methods=["POST"])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
        
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_service_ticket = ServiceTickets(**service_ticket_data)
    db.session.add(new_service_ticket)
    db.session.commit()

    return service_ticket_schema.jsonify(new_service_ticket), 201


#========== Read ===========


@service_ticket_bp.route("/<int:service_ticket_id>", methods=["GET"])
def get_service_ticket(service_ticket_id):
    try:
        service_ticket_data = db.session.get(ServiceTickets, service_ticket_id)
        
    except ValidationError as err:
        return jsonify(err.messages), 400
     

    return service_ticket_schema.jsonify(service_ticket_data), 200


@service_ticket_bp.route("/", methods=["GET"])
def get_service_ticket_bps():
    try:
        service_ticket_bps_data = db.session.query(ServiceTickets).all()
        
    except ValidationError as err:
        return jsonify(err.messages), 400
     

    return service_ticket_schema.jsonify(service_ticket_bps_data), 200


#========== Update ===========


@service_ticket_bp.route("/<int:service_ticket_id>", methods=["PUT"])
def update_service_ticket(service_ticket_id):
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    service_ticket = db.session.get(ServiceTickets, service_ticket_id)
    if not service_ticket:
        return jsonify({"error": "service_ticket not found"}), 404

    service_ticket.name = service_ticket_data.get("name", service_ticket.name)
    service_ticket.email = service_ticket_data.get("email", service_ticket.email)
    service_ticket.address = service_ticket_data.get("address", service_ticket.address)

    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200


#========== Delete ===========


@service_ticket_bp.route("/<int:service_ticket_id>", methods=["DELETE"])
def delete_service_ticket(service_ticket_id):
    service_ticket = db.session.get(ServiceTickets, service_ticket_id)
    if not service_ticket:
        return jsonify({"error": "service_ticket not found"}), 404

    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"message": "service_ticket deleted"}), 200

