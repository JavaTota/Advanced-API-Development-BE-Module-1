from marshmallow import fields

from application.blueprints.mechanics.schemas import MechanicSchema
from application.extensions import ma
from application.models import ServiceTicket

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested(MechanicSchema, many=True)
    class Meta:
        model = ServiceTicket
        include_fk = True
        

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)