from application.blueprints.mechanics.schemas import MechanicSchema
from application.extensions import ma
from application.models import ServiceTicket

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = ma.List(ma.Nested(lambda: MechanicSchema(only=("id", "name"))))
    class Meta:
        model = ServiceTicket
        include_fk = True
        

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)