from marshmallow import fields

from application.blueprints.mechanics.schemas import MechanicSchema
from application.extensions import ma
from application.models import  Inventory, ServiceTicketInventory

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory

    def get_ticket_count(self, obj):
        return len(obj.service_tickets)
    
class ServiceTicketInventorySchema(ma.SQLAlchemyAutoSchema):
    inventory = fields.Nested(InventorySchema, only=("id", "name", "price"))

    class Meta:
        model = ServiceTicketInventory

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)