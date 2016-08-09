import uuid


class Orders:
    ''' Create a new order'''
    def __init__(self, customer_id):
        self.order_id = uuid.uuid4().int
        self.payment_option_id = None
        self.customer_id = customer_id
        self.paid_in_full = False
