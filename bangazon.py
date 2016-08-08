import pickle
from customers import *
from order_line_items import *
from orders import *
from payment_options import *
from product import *

class Bangazon:
    ''' Calls other modules to set users and serialize/deserialize data.
    '''
    def __init__(self):
        ''' Initialize '''
        self.current_customer = None
        self.deserialize()

    def create_customer(self, name, address, city, state, zip_code, phone):
        '''Create and save a new instance of customers'''
        customer = Customer(name, address, city, state, zip_code, phone)
        self.customers[customer.customer_id] = customer
        self.set_current_customer(customer)
        self.serialize('customers.txt', self.customers)

    def create_payment_option(self, name, account_number):
        option = PaymentOption()


    def set_current_customer(self, customer):
        '''Sets new user as current user'''
        self.current_customer = customer

    def serialize(self, file_name, data):
        ''' serialize files.'''
         """ Serializes data to a file

        Method arguments:
        -----------------
        file_name(str) -- The file name that will be serialized to
        data(obj) -- The data to be serialized
        """
        with open(file_name, 'wb+') as f:
            pickle.dump(data, f)

    def deserialize(self):
        ''' deserialize files. If error, set values to empty string'''
        try:
            with open('customers.txt', 'rb+') as f:
                self.customers = pickle.load(f)
        except:
            self.customers = {}

        try:
            with open('orders.txt', 'rb+') as f:
                self.orders = pickle.load(f)
        except:
            self.orders = {}

        try:
            with open('product.txt', 'rb+') as f:
                self.product = pickle.load(f)
        except:
            self.product = {}

        try:
            with open('payment_options.txt', 'rb+') as f:
                self.payment_options = pickle.load(f)
        except:
            self.payment_options = {}

        try:
            with open('order_line_items.txt', 'rb+') as f:
                self.order_line_items = pickle.load(f)
        except:
            self.order_line_items = {}
