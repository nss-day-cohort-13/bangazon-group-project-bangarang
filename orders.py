import uuid
from customers import *

class Orders:
    ''' Create a new order'''
    def __init__(self, payment_option_id, customer_id, paid_in_full=False):
        self.order_id = uuid.uuid4().int
        self.payment_option_id = payment_option_id
        self.customer_id = customer_id
        self.paid_in_full = paid_in_full
