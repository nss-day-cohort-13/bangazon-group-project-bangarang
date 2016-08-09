import uuid


class Customer:
    ''' Create a new customer'''
    def __init__(self, name, address, city, state, zip_code, phone):
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone = phone
        self.obj_id = uuid.uuid4().int
        self.payment_option_ids = []