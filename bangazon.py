import pickle
import sqlite3

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

def get_all_products():
    with sqlite3.connect('bangazon.db') as conn:
      c = conn.cursor()
      c.execute("SELECT * FROM Product")
      conn.commit()
      return c.fetchall()

def get_all_customers():
    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()
        c.execute('select * from Customer')
        conn.commit()
        return c.fetchall()

def create_new_customer(name, address, city, state, zip_code):
    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()
        c.execute('''insert into Customer(name, address, city, state, zip_code)
        values(?, ?, ?, ?, ?)''', (name, address, city, state, zip_code))
        conn.commit()
        return c.lastrowid

def create_new_order_line_item(order_id, product_id):
    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO OrderLineItem (order_id, product_id) VALUES (?, ?)",
                    (order_id, product_id))
        conn.commit()

def get_product_id_list_per_order(order_id):
    with sqlite3.connect('bangazon.db') as conn:
      c = conn.cursor()
      c.execute("SELECT product_id FROM OrderLineItem WHERE order_id={0}".format(order_id))
      conn.commit()
      return c.fetchall()

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


def create_new_order():
    global current_customer_id
    global current_order_id

    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()

        c.execute("insert into Orders (customer_id) values (?)",
                  (current_customer_id))

        # sets the current_order_id as the
        current_order_id = c.lastrowid

        conn.commit()


def get_product_names_per_order_for_current_user():
    global current_customer_id
    global current_order_id

    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()

        c.execute("""SELECT o.order_id, GROUP_CONCAT (p.name, ", ") as Products
                  FROM OrderLineItem oli
                  INNER JOIN Product p ON oli.product_id = p.product_id
                  INNER JOIN Orders o ON oli.order_id = o.order_id
                  WHERE o.customer_id = ?
                  GROUP BY o.order_id""", (current_customer_id))

        c.commit()
        return c.fetchall()
