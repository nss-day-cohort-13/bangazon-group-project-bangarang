import sqlite3


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
        c.execute('''insert into Customer(name, address, city, state_of_residence, zip_code)
        values(?, ?, ?, ?, ?)''', (name, address, city, state, zip_code))
        conn.commit()
        return c.lastrowid


def get_customer_per_customer_id(customer_id):
    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()  #cursor extracts table and holds results with data
        c.execute("SELECT * FROM Customer WHERE customer_id=?", (customer_id,))
        customer = c.fetchall()
        current_customer = customer[0][1]
        return current_customer

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


def create_new_payment_option(name, account_number, current_customer_id):
    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()  #cursor extracts table and holds results with data
        c.execute("INSERT INTO PaymentOption VALUES (?,?,?,?)",
                  (None, name, account_number, current_customer_id))
        conn.commit()
        return c.fetchall()  #sqlite3 function to return all results


def get_payment_options_per_customer(customer_id):
    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()  #cursor extracts table and holds results with data
        c.execute("SELECT name FROM PaymentOption WHERE customer_id={0}".format(customer_id))
        all_payment_options = c.fetchall()
        print(all_payment_options)  #sqlite3 function to return all results


def create_new_order(customer_id):

    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()

        c.execute("INSERT INTO Orders (customer_id) VALUES (?)",
                  (customer_id,))

        conn.commit()

        return c.lastrowid


def get_product_names_per_order_for_current_user(customer_id):

    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()

        c.execute("""SELECT o.order_id, GROUP_CONCAT (p.name, ", ") as Products
                  FROM OrderLineItem oli
                  INNER JOIN Product p ON oli.product_id = p.product_id
                  INNER JOIN Orders o ON oli.order_id = o.order_id
                  WHERE o.customer_id = ?
                  GROUP BY o.order_id""", (customer_id,))

        c.commit()
        return c.fetchall()


def finalize_order(payment_option_id, order_id):

    with sqlite3.connect('bangazon.db') as conn:
        c = conn.cursor()

        c.execute("""UPDATE Orders
                  SET payment_options_id = ?, paid_in_full = 1
                  WHERE order_id = ?""",
                  (payment_option_id, order_id))

        c.commit()
