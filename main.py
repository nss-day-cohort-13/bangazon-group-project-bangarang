import bangazon
import customer_class
import order_class
import payment_options_class
import order_line_item_class
import line_item_report
import order_line_item_class
import locale
import os

current_customer = None
current_order = None

def generate_main_menu():
    '''
    Generates main menu string
    '''
    output = ('\n\033[94m\033[1m 1. Create A Customer Account' +
    '\n 2. Choose Active Customer' +
    '\n 3. Create A Payment Option' +
    '\n 4. Add Product To Shopping Cart' +
    '\n 5. Complete An Order' +
    '\n 6. See Product Popularity' +
    '\n 7. Leave Bangazon')
    return output

def run_create_user():
    '''
    Creates a new customer,
    sets the current_user to be the new customer,
    updates serialized customer dictionary
    '''
    global current_customer
    clear_menu()
    name = input('\n Name: ')
    address = input('\n Address: ')
    city = input('\n City: ')
    state = input('\n State: ')
    zip_code = input('\n Zip Code: ')
    phone = input('\n Phone: ')
    new_customer = customer_class.Customer(name, address, city, state, zip_code, phone)
    bangazon.update_serialized_data('customers.txt', new_customer)
    current_customer = new_customer
    runner()

def run_select_user():
    '''
    Displays list of customer names,
    gets user input to select customer
    and sets global current_customer
    '''
    global current_customer
    clear_menu()
    stored_customers = bangazon.deserialize('customers.txt')
    stored_customers_list = list()
    print('Select User:')
    for key, customer_id in enumerate(stored_customers):
        customer = stored_customers[customer_id]
        stored_customers_list.append(customer.obj_id)
        print('\n {0}. {1}'.format(key + 1, customer.name))
    user_input = int(input('\n > '))
    current_customer = stored_customers[stored_customers_list[user_input - 1]]
    # print('\n Welcome {0}'.format(current_customer.name))
    runner()

def run_create_payment():
    '''
    Deserialize stored payment dictionary,
    create new payment option from user input,
    and update serialized payment dictionary
    '''
    global current_customer
    clear_menu()
    stored_payments = bangazon.deserialize('payments.txt')
    stored_payments_list = list()
    print(' Enter payment information below:')
    name = input(' Name: ')
    account_number = input(' Card Number: ')
    new_payment_option = payment_options_class.PaymentOption(name, account_number, current_customer.obj_id)
    current_customer.payment_option_ids.append(new_payment_option.obj_id)
    bangazon.update_serialized_data('customers.txt', current_customer)
    bangazon.update_serialized_data('payments.txt', new_payment_option)
    runner()

def run_select_unpaid_order(new_order_option=False):
    """ Displays all unpaid orders for the user that is currently logged in,
    and allows them to select which one they want. Will call the method to add products to
    an order if the new_order_option is True, or will call the method to finalize an order.

    Method arguments:
    -----------------
    new_order_option(boolean) -- When True, displays the option to create a new order, then calls the
                                 run_add_products method after user selection.
                                 If false, calls the run_complete_order method.
                                 Defaults to False.
    """
    global current_customer
    global current_order
    global stored_products
    user_input = ''

    clear_menu()
    stored_orders = bangazon.deserialize('orders.txt')
    stored_order_line_items = bangazon.deserialize('order_line_items.txt')

    # gets all orders that belong to the customer logged in and have not yet been paid
    current_customer_orders = [order for order in stored_orders.values()
                               if order.customer_id == current_customer.obj_id and
                               order.paid_in_full is False]

    for key, order in enumerate(current_customer_orders):
        # gets the first 5 order_line items' product ids that correspond to the current order
        order_items = [item.product_id for item in stored_order_line_items.values()
                       if item.order_id == order.obj_id][0:5]

        # gets the names of each product for the ids stored in order_items
        product_names_to_display = [stored_products[order_item].name for order_item in order_items]
        # send message to menu if there are no products in an order
        if len(product_names_to_display) == 0:
            product_names_to_display = ["No products added yet"]

        print('\n {0}. {1}'.format(key + 1, ", ".join(product_names_to_display)))

    # display New Order option if True, otherwise don't print it
    if new_order_option:
        print('\n 100. Start New Order')

    print('\n 0. Cancel')

    # get user input in integer form
    try:
        user_input = int(input("\n > "))

    except ValueError:
        print("\nError: Input must be an integer. Please try again.")
        run_add_products()

    if user_input == 0:
        runner()

    if new_order_option and user_input == 100:
        # creates a new order and sets it as the global current_order and saves the data
        current_order = order_class.Order(current_customer.obj_id)
        bangazon.update_serialized_data('orders.txt', current_order)

    else:
        try:
            current_order = current_customer_orders[user_input - 1]

        except IndexError:
            print("\nError: Input must be the number value next to the option you wish to select.")
            run_select_unpaid_order()

    # if the new order option is true, go to menu to add products to the order,
    # otherwise go to the menu to complete an order
    if new_order_option:
        run_add_products()

    else:
        run_complete_order()

def run_add_products():
    """ Displays all products and prices, and
    lets a user select a product to add to their current shopping cart.

    Method arguments:
    -----------------
    n/a
    """
    global stored_products
    global current_order

    stored_products_list = list()

    print("\n Select products to add to your order:\n")
    # displays all available products and prices,
    # and creates an ordered list to compare with the user's input
    for key, product in enumerate(stored_products.values()):
        stored_products_list.append(product)
        print('\n {0}. {1} {2}'.format(key + 1, product.name, product.price))
    print('\n 0. Done Adding Products')

    try:
        user_input = int(input("\n > "))

    except ValueError:
        print("\nError: Input must be an integer. Please try again.")
        run_add_products()

    if user_input == 0:
        runner()

    else:
        try:
            # gets the product selcted by the user and creates an
            # order line item with it's id and the current order id
            selected_product = stored_products_list[user_input - 1]
            new_order_line_item = order_line_item_class.OrderLineItem(current_order.obj_id, selected_product.obj_id)
            bangazon.update_serialized_data('order_line_items.txt', new_order_line_item)

        except IndexError:
            print("\nError: Input must be an integer in the range of options.")

        run_add_products()



def run_complete_order():
    """ Displays the total for the chosen order and then lets your choose your
    payment option

    Method arguments:
    -----------------
    n/a
    """
    global stored_products
    global current_customer
    global current_order

    clear_menu()
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    stored_order_line_items = bangazon.deserialize('order_line_items.txt')
    order_to_be_paid = current_order.obj_id
    products_in_order = [value for key,value in stored_order_line_items.items()
        if order_to_be_paid == value.order_id]
    product_ids = [item.product_id for item in products_in_order]
    product_prices = [stored_products[id].price for id in product_ids]
    format_int_prices = [float(item.replace(',','')[1:]) for item in product_prices]
    total = 0
    for item in format_int_prices:
        total = total + item
    formatted_total = locale.currency(total, grouping=True)
    print('Your order total is ' + formatted_total + '. Ready to purchase')
    choice = input('Y/N > ')
    if choice == 'Y' or choice == 'y':
        all_payment_options = bangazon.deserialize('payments.txt')

        # if customer has no payment options, send them to the create payment option menu
        if len(current_customer.payment_option_ids) == 0:
            print("\nYou must add a payment option before checking out.")
            run_create_payment()

        customer_payment_options = current_customer.payment_option_ids
        payment_options = [all_payment_options[item] for item in customer_payment_options]
        for key, payment in enumerate(payment_options):
            print('\n{0}. {1}'.format(key + 1, payment.name))
        print('0. Cancel')
        selection = int(input('What is your choice? > '))
        if selection >= 1:
            try:
                current_order.paid_in_full = True
                current_order.payment_option_id = payment_options[selection - 1].obj_id
                bangazon.update_serialized_data('orders.txt', current_order)
                print('\nYou chose {0}'.format(payment_options[selection - 1].name))
                print('\n Your order is complete!')
                runner()
            except:
                print('Error: Invalid input.')
                run_complete_order()
        if selection < 1:
            runner()
    if choice == 'N' or choice == 'n':
        runner()




def initialize():
    global stored_products
    stored_products = bangazon.deserialize('products.txt')

def clear_menu():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def runner():
    initialize()
    clear_menu()
    if current_customer != None:
        print('\n Current User: ' + current_customer.name)
    print('\n Input option number:')
    print(generate_main_menu())
    user_input = input('\n > ')
    if user_input == '1':
        run_create_user()
        runner()
    elif user_input == '2':
        run_select_user()
        runner()
    elif user_input == '3':
        run_create_payment()
        runner()
    elif user_input == '4':
        run_select_unpaid_order(True)
        runner()
    elif user_input == '5':
        run_select_unpaid_order()
        runner()
    elif user_input == '6':
        print(line_item_report.generate_product_popularity_report())
        runner()
    elif user_input == '7':
        exit()


if __name__ == '__main__':
    runner()
