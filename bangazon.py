import sqlite3

# select products from database
def get_all_products():
    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Product")
        conn.commit()
        return c.fetchall()

# select customers from database
def get_all_customers():
    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()
        c.execute('select * from Customer')
        conn.commit()
        return c.fetchall()

# create a new customer and add to database
def create_new_customer(name, address, city, state, zip_code):
    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()
        c.execute('''insert into Customer(name, address, city, state_of_residence, zip_code)
        values(?, ?, ?, ?, ?)''', (name, address, city, state, zip_code))
        conn.commit()
        return c.lastrowid

# get customer ID from database
def get_customer_per_customer_id(customer_id):
    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()  #cursor extracts table and holds results with data
        c.execute("SELECT * FROM Customer WHERE customer_id=?", (customer_id,))
        customer = c.fetchall()
        current_customer = customer[0][1]
        return current_customer

# Insert order and product ID's into database
def create_new_order_line_item(order_id, product_id):
    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO OrderLineItem (order_id, product_id) VALUES (?, ?)",
                  (order_id, product_id))
        conn.commit()

# get product ID from database
def get_product_id_list_per_order(order_id):
    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()
        c.execute("SELECT product_id FROM OrderLineItem WHERE order_id={0}".format(order_id))
        conn.commit()
        return c.fetchall()

# add new payment options to database
def create_new_payment_option(name, account_number, current_customer_id):
    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()  #cursor extracts table and holds results with data
        c.execute("INSERT INTO PaymentOption VALUES (?,?,?,?)",
                  (None, name, account_number, current_customer_id))
        conn.commit()
        return c.fetchall()  #sqlite3 function to return all results

# get payment options from database for a given customer
def get_payment_options_per_customer(customer_id):
    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()  #cursor extracts table and holds results with data
        c.execute("SELECT payment_option_id, name FROM PaymentOption WHERE customer_id={0}".format(customer_id))
        all_payment_options = c.fetchall()
        return(all_payment_options)  #sqlite3 function to return all results

def get_prices_in_order(order_id):
    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()

        c.execute("""SELECT p.price
                  FROM
                    Orders o
                  INNER JOIN OrderLineItem oli ON o.order_id = oli.order_id
                  INNER JOIN Product p ON oli.product_id = p.product_id
                  WHERE o.order_id = ?""",
                  (order_id,))
        return c.fetchall()

def create_new_order(customer_id):
    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()

        c.execute("INSERT INTO Orders (customer_id) VALUES (?)",
                  (customer_id,))

        conn.commit()

        return c.lastrowid

# get products from an order for a given customer
def get_product_names_per_order_for_current_user(customer_id):
    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()

        c.execute("""SELECT o.order_id, GROUP_CONCAT (p.name, ", ") as Products
                  FROM OrderLineItem oli
                  INNER JOIN Product p ON oli.product_id = p.product_id
                  INNER JOIN Orders o ON oli.order_id = o.order_id
                  WHERE o.customer_id = ?
                  AND o.paid_in_full = 0
                  GROUP BY o.order_id""", (customer_id,))

        conn.commit()
        return c.fetchall()

# complete order
def finalize_order(payment_option_id, order_id):

    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()

        c.execute("""UPDATE Orders
                  SET payment_options_id = ?, paid_in_full = 1
                  WHERE order_id = ?""",
                  (payment_option_id, order_id))

        conn.commit()
