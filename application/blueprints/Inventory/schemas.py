from marshmallow import fields

from application.blueprints.mechanics.schemas import MechanicSchema
from application.extensions import ma
from application.models import  Inventory

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory

    def get_ticket_count(self, obj):
        return len(obj.service_tickets)

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)