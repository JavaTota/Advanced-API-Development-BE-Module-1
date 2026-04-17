from marshmallow import fields

from application.blueprints.mechanics.schemas import MechanicSchema
from application.extensions import ma
from application.models import ServiceTicket

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested(MechanicSchema, many=True)
    class Meta:
        model = ServiceTicket
        include_fk = True

# This schema will be used for updating service tickets, allowing us to specify which mechanics to add or remove from a ticket without needing to provide all the other fields.
class ServiceTicketUpdateSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Integer(), required=True)
    remove_mechanic_ids = fields.List(fields.Integer(), required=True)

    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
service_ticket_update_schema = ServiceTicketUpdateSchema()