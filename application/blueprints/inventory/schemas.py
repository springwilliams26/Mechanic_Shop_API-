from application.extensions import ma
from application.models import Inventory


class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = False


inventory_schema = InventorySchema()
inventory_items_schema = InventorySchema(many=True)