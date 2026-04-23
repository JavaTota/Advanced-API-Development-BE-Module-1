from marshmallow import fields

from application.blueprints.Inventory.schemas import InventorySchema, ServiceTicketInventorySchema
from application.blueprints.mechanics.schemas import MechanicSchema
from application.extensions import ma
from application.models import ServiceTicket

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested(MechanicSchema, many=True)
    ticket_inventory = fields.Nested(ServiceTicketInventorySchema, many=True)
    class Meta:
        model = ServiceTicket
        include_fk = True
        dump_only = ("id", "service_date") # We set service_date to dump_only because we want it to be automatically set to the current date and time when a new service ticket is created, rather than being provided by the client in the request data.

# This schema will be used for updating service tickets, allowing us to specify which mechanics to add or remove from a ticket without needing to provide all the other fields.
class ServiceTicketUpdateSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Integer())
    remove_mechanic_ids = fields.List(fields.Integer())

    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
service_ticket_update_schema = ServiceTicketUpdateSchema()