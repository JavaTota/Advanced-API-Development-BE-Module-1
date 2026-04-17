from marshmallow import fields

from application.extensions import ma
from application.models import  Mechanic

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    ticket_count = fields.Method("get_ticket_count")
    class Meta:
        model = Mechanic

    def get_ticket_count(self, obj):
        return len(obj.service_tickets)

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)