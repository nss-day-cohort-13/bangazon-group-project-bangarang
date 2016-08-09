import pickle
# import customers as customer_class
# from order_line_items import *
# from orders import *
# from payment_options import *
# from product import *

# current_customer = None

# def create_customer(name, address, city, state, zip_code, phone):
#     global customers
#     """ Creates a new customer,
#     sets the current_user to be the new customer,
#     adds the new customer data to the customers dictionary
#     using the new customer's UUID as a key,
#     and serializes the customers dictionary
#
#     Method arguments:
#     -----------------
#     name(str) -- What the new customer's name attribute will be
#     address(str) -- What the new customer's address attribute will be
#     city(str) -- What the new customer's city attribute will be
#     state(str) -- What the new customer's state attribute will be
#     zip_code(int) -- What the new customer's zip_code attribute will be
#     phone(str) -- What the new customer's phone attribute will be
#     """
#     customer = customer_class.Customer(name, address, city, state, zip_code, phone)
#     customers[customer.customer_id] = customer
#     set_current_customer(customer)
#     serialize('customers.txt', customers)
#
# def create_payment_option(name, account_number):
#     global options
#     global customers
#     global payment_options
#     global current_customer
#     """ Creates a new payment option.
#     Sets the name of account and account number attributes.
#     Adds the new payment option data to the payment_options dictionary
#     using the new payment option's UUID as a key,
#     and serializes the payment_options dictionary
#
#     Method arguments:
#     -----------------
#     name(str) -- What the new payment option's name is
#     account_number(int) -- What the new payment options's account number is
#     """
#     options = PaymentOption(name, account_number)
#     payment_options.update({option.payment_option_id: option})
#
#     # saves the new payment option
#     serialize(payment_options.txt, payment_options)
#
#     # update the current customer's payment ids and
#     # overwrites their info in the list of customers, then saves the updated list
#     current_customer.payment_option_ids.append(option.payment_option_id)
#     custormers.update({current_customer.customer_id: current_customer})
#     serialize(customers.txt, custormers)
#
# def create_new_order():
#     pass
#
# def set_current_customer(customer):
#     global current_customer
#     '''Sets new user as current user'''
#     current_customer = customer

def serialize(file_name, data):
    """ Serializes data to a file

    Method arguments:
    -----------------
    file_name(str) -- The file name that will be serialized to
    data(obj) -- The data to be serialized
    """
    with open(file_name, 'wb+') as f:
        pickle.dump(data, f)

def deserialize(file):
    stored_obj_dict = dict()
    try:
        with open(file, 'rb+') as f:
            stored_obj_dict = pickle.load(f)
    except:
        stored_dict = {}
    return stored_obj_dict

def update_serialized_data(file, new_object):
    stored_dict = deserialize(file)
    stored_dict.update({new_object.obj_id: new_object})
    serialize(file, stored_dict)


# def deserialize():
#     """ Deserializes customers.txt, orders.txt, and products.txt,
#     payment_options.txt, and order_line_items.txt
#     and sets the custormers, orders, products,
#     payment_options, and order_line_items
#     attributes to the data respectively.
#     If an error occurs desirializing any of the files,
#     the attribute value will be set to an empty dictionary
#
#     Method arguments:
#     -----------------
#     n/a
#     """
#     global customers
#     global orders
#     global products
#     global payment_options
#     global line_items
#
#     try:
#         with open('customers.txt', 'rb+') as f:
#             customers = pickle.load(f)
#     except:
#         customers = {}
#
#     try:
#         with open('orders.txt', 'rb+') as f:
#             orders = pickle.load(f)
#     except:
#         orders = {}
#
#     try:
#         with open('product.txt', 'rb+') as f:
#             products = pickle.load(f)
#     except:
#         producst = {}
#
#     try:
#         with open('payment_options.txt', 'rb+') as f:
#             payment_options = pickle.load(f)
#     except:
#         payment_options = {}
#
#     try:
#         with open('order_line_items.txt', 'rb+') as f:
#             order_line_items = pickle.load(f)
#     except:
#         order_line_items = {}
