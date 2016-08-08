import uuid
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.product_id = uuid.uuid4().int
