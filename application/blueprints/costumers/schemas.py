from application.extensions import ma
from application.models import Costumer

class CostumerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Costumer

costumer_schema = CostumerSchema()
costumers_schema = CostumerSchema(many=True)