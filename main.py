import bangazon
import customer_class
import order_class
import payment_options_class


current_customer = None


def generate_main_menu():
    output = ('\n\033[94m\033[1m 1. Create A Customer Account' +
    '\n 2. Choose Active Customer' +
    '\n 3. Create A Payment Option' +
    '\n 4. Add Product To Shopping Cart' +
    '\n 5. Complete An Order' +
    '\n 6. See Product Popularity' +
    '\n 7. Leave Bangazon')
    return output

def run_create_user():
    name = input('\n Name: ')
    address = input('\n Address: ')
    city = input('\n City: ')
    state = input('\n State: ')
    zip_code = input('\n Zip Code: ')
    phone = input('\n Phone: ')
    new_customer = customer_class.Customer(name, address, city, state, zip_code, phone)
    bangazon.update_serialized_data('customers.txt', new_customer)

def run_select_user():
    global current_customer
    stored_customers = bangazon.deserialize('customers.txt')
    output = str()
    stored_customers_list = list()
    print('Select User:')
    for key, customer_id in enumerate(stored_customers):
        customer = stored_customers[customer_id]
        stored_customers_list.append(customer.obj_id)
        print('\n {0}. {1}'.format(key + 1, customer.name))
    user_input = int(input('\n > '))
    current_customer = stored_customers[stored_customers_list[user_input - 1]]
    print('\n Welcome {0}'.format(current_customer.name))
    runner()

def run_create_payment():
    global current_customer
    stored_payments = bangazon.deserialize('payments.txt')
    stored_payments_list = list()
    print(' Enter payment information below:')
    name = input(' Name: ')
    account_number = input(' Card Number: ')
    new_payment_option = payment_options_class.PaymentOption(name, account_number, current_customer.obj_id)
    bangazon.update_serialized_data('payments.txt', new_payment_option)

def run_select_unpaid_order(new_order_option=False):
    global current_customer
    global current_order
    global stored_products

    stored_orders = bangazon.deserialize('orders.txt')
    stored_order_line_items = bangazon.deserialize('order_line_items.txt')

    # gets all orders that belong to the customer logged in and have not yet been paid
    current_customer_orders = [order for order in stored_orders.values()
                               if order.customer_id == current_customer.obj_id and
                               order.paid_in_full is False]

    for key, order in enumerate(current_customer_orders):
        # gets the first 5 order_line items' product ids that correspond to the current order
        order_items = [item.product_id for key, item in enumerate(stored_order_line_items)
                       if item.order_id == order.obj_id and
                       key <= 4]

        # gets the names of each product for the ids stored in order_items
        product_names_to_display = [stored_products[order_item] for order_item in order_items]

        # send message to menu if there are no products in an order
        if len(product_names_to_display) == 0:
            product_names_to_display = ["No products added yet"]

        print('\n {0}. {1}'.format(key + 1, ",".join(product_names_to_display)))

    # display New Order option if True, otherwise don't print it
    if new_order_option:
        print('\n 0. Start New Order')

    # get user input in integer form
    try:
        user_input = int(input("\n > "))

    except ValueError:
        print("\nError: Input must be an integer. Please try again.")
        run_add_products()

    if new_order_option:
        if user_input == 0:
            # creates a new order and sets it as the global current_order and saves the data
            current_order = order_class.Order(current_customer.obj_id)
            bangazon.update_serialized_data('orders.txt', current_order)

    try:
        current_order = current_customer_orders[user_input - 1]

    except IndexError:
        print("\nError: Input must be the number value next to the option you wish to select.")

    # if the new order option is true, go to menu to add products to the order,
    # otherwise go to the menu to complete an order
    if new_order_option:
        run_add_products()

    else:
        run_complete_order()


def run_add_products():
    pass
    # global stored_products
    # print("Select products to add to your order:\n")

def run_complete_order():
    pass

def initialize():
    global stored_products
    stored_products = bangazon.deserialize('products.txt')

def runner():
    initialize()
    print('\n Input option number:')
    print(generate_main_menu())
    user_input = input('\n > ')
    if user_input == '1':
        run_create_user()
    elif user_input == '2':
        run_select_user()
    elif user_input == '3':
        run_create_payment()
    elif user_input == '4':
        run_select_unpaid_order(True)
    elif user_input == '5':
        run_select_unpaid_order
    elif user_input == '6':
        run_generate_popularity_report()
    elif user_input == '7':
        pass

if __name__ == '__main__':
    runner()
