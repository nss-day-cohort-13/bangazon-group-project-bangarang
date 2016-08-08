import uuid


class PaymentOption():

    def __init__(self, name, account_number):
        """ Sets the name, account_number attributes on creation of a new instance
        and sets payment_id as an integer UUID

        Method arguments:
        -----------------
        name(str) -- The name of the payment option
        account_number(int) -- The payment option account number
        """
        self.name = name
        self.account_number = account_number
        self.payment_id = uuid.uuid4().int
