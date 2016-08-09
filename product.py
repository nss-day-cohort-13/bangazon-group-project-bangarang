import uuid
class Product:
    def __init__(self, name, price):
        """ sets inital values for product name, price and prdouct_id"""
        self.name = name
        self.price = price
        self.product_id = uuid.uuid4().int
