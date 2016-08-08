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
        """ Creates a new customer,
        sets the current_user to be the new customer,
        adds the new customer data to the self.customers dictionary
        using the new customer's UUID as a key,
        and serializes the self.customers dictionary

        Method arguments:
        -----------------
        name(str) -- What the new customer's name attribute will be
        address(str) -- What the new customer's address attribute will be
        city(str) -- What the new customer's city attribute will be
        state(str) -- What the new customer's state attribute will be
        zip_code(int) -- What the new customer's zip_code attribute will be
        phone(str) -- What the new customer's phone attribute will be
        """
        customer = Customer(name, address, city, state, zip_code, phone)
        self.customers[customer.customer_id] = customer
        self.set_current_customer(customer)
        self.serialize('customers.txt', self.customers)

    def create_payment_option(self, name, account_number):
        """ Creates a new payment option.
        Sets the name of account and account number attributes.
        Adds the new payment option data to the self.payment_options dictionary
        using the new payment option's UUID as a key,
        and serializes the self.payment_options dictionary

        Method arguments:
        -----------------
        name(str) -- What the new payment option's name is
        account_number(int) -- What the new payment options's account number is
        """
        option = PaymentOption(name, account_number)
        self.payment_options[option.payment_option_id] = option
        self.current_customer.payment_option_ids.append(option.payment_option_id)

        # saves the new payment option
        self.serialize(payment_options.txt, self.payment_options)

        # update the current customer's payment ids and
        # overwrites their info in the list of customers, then saves the updated list
        self.custormers[self.current_customer.customer_id] = self.current_customer
        self.serialize(customers.txt, self.custormers)

    def set_current_customer(self, customer):
        '''Sets new user as current user'''
        self.current_customer = customer

    def serialize(self, file_name, data):
        """ Serializes data to a file

        Method arguments:
        -----------------
        file_name(str) -- The file name that will be serialized to
        data(obj) -- The data to be serialized
        """
        with open(file_name, 'wb+') as f:
            pickle.dump(data, f)

    def deserialize(self):
        """ Deserializes customers.txt, orders.txt, and products.txt,
        payment_options.txt, and order_line_items.txt
        and sets the self.custormers, self.orders, self.products,
        self.payment_options, and self.order_line_items
        attributes to the data respectively.
        If an error occurs desirializing any of the files,
        the attribute value will be set to an empty dictionary

        Method arguments:
        -----------------
        n/a
        """
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
