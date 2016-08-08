import uuid


class OrderLineItem():

    def __init__(self, order_id, product_id):
        """ Sets the order_id and product_id attributes on creation of a new instance
        and sets order_line_item_id as an integer UUID

        Method arguments:
        -----------------
        order_id(int) -- The uuid of the order
        product_id(int) -- The uuid of the product
        """
        self.order_id = order_id
        self.product_id = product_id
        self.order_line_item_id = uuid.uuid4().int
