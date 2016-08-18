import bangazon
# import customer_class
# import order_class
# import payment_options_class
# import order_line_item_class
import line_item_report
# import order_line_item_class
import locale
import os
import sqlite3

current_customer_id = None
current_order_id = None


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
    sets the current_customer to be the new customer
    '''
    global current_customer_id
    clear_menu()
    name = input('\n Name: ')
    address = input('\n Address: ')
    city = input('\n City: ')
    state = input('\n State: ')
    zip_code = input('\n Zip Code: ')
    customer_id = bangazon.create_new_customer(name, address, city, state, zip_code)
    current_customer_id = customer_id
    runner()

def run_select_user():
    '''
    Displays list of customer names,
    gets user input to select customer
    and sets global current_customer
    '''
    global current_customer_id
    clear_menu()
    stored_customers = bangazon.get_all_customers()
    print('Select User:')
    for number, customer in enumerate(stored_customers, start=1):
        print(str(number)) + ".) " + customer[1]
    choice = int(input('Who do you choose > '))
    current_customer_id = stored_customers[choice - 1][0]
    runner()


def run_create_payment():
    '''
    Deserialize stored payment dictionary,
    create new payment option from user input,
    and update serialized payment dictionary
    '''
    global current_customer_id
    clear_menu()
    print(' Enter payment information below:')
    name = input(' Name: ')
    account_number = input(' Card Number: ')
    bangazon.create_new_payment_option(name, account_number, current_customer_id)
    runner()

def run_select_unpaid_order(complete_an_order=False):
    """ Displays all unpaid orders for the user that is currently logged in,
    and allows them to select which one they want. Will call the method to add products to
    an order if the complete_an_order is True, or will call the method to finalize an order.

    Method arguments:
    -----------------
    complete_an_order(boolean) -- When True, displays the option to create a new order, then calls the
                                 run_add_products method after user selection.
                                 If false, calls the run_complete_order method.
                                 Defaults to False.
    """
    global current_customer_id
    global current_order_id
    clear_menu()

    products_in_orders = bangazon.get_product_names_per_order_for_current_user(current_customer_id)

    for key, order in enumerate(products_in_orders):
        print('\n {0}. {1}'.format(key + 1, order[1]))

    if complete_an_order:

        print('\n 100. Start New Order')

    print('\n 0. Cancel')

    try:
        user_input = int(input(' > '))
    except ValueError:
        print("\nError: Incorrect input. Please try again.")
        if complete_an_order:
            run_select_unpaid_order()
        else:
            run_select_unpaid_order(True)

    # what actions to perform based on user input
    if user_input == 0:
        runner()

    elif complete_an_order and user_input == 100:
        current_order_id = bangazon.create_new_order(current_customer_id)

    else:
        current_order_id = products_in_orders[user_input - 1][0]

    # calls next menu based on complete_an_order
    if complete_an_order:
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
    global current_order_id

    clear_menu()

    print("\n Select products to add to your order:\n")

    products = bangazon.get_all_products()

    for key, product in enumerate(products):
        print('\n {0}. {1} ${2}'.format(key + 1, product[1], product[2]))

    print('\n 0. Done')

    try:
        user_input = int(input(' > '))

    except ValueError:
        print("\nError: Invalid input. Please try again.")
        run_add_products()

    # what actions to perform based on user input
    if user_input == 0:
        runner()

    else:
        selected_product_id = products[user_input - 1][0]

        bangazon.create_new_order_line_item(current_order_id,
                                            selected_product_id)
        run_add_products()


def run_complete_order():
    """ Displays the total for the chosen order and then lets your choose your
    payment option

    Method arguments:
    -----------------
    n/a
    """
    global current_customer_id
    global current_order_id

    clear_menu()

    prices = bangazon.get_prices_in_order(current_order_id)

    total_price = sum([int(price[0]) for price in prices])

    print("Your order total is ${0}. Ready to purchase?".format(total_price))
    ready_to_purchase = input('\nY/N > ')

    if ready_to_purchase.lower() == 'y':

        print("\nSelect a Payment Option:")

        payment_options = bangazon.get_payment_options_per_customer(current_customer_id)

        if payment_options == []:
            print("\nPlease add a payment option before completing an order.")
            print("\nPress enter to continue.")
            input("")
            run_create_payment()

        for key, option in enumerate(payment_options):
            print('\n {0}. {1}'.format(key + 1, option[1]))

        user_input = int(input("\n > "))

        selected_payment_option_id = payment_options[user_input - 1][0]
        bangazon.finalize_order(selected_payment_option_id, current_order_id)
        runner()

    elif ready_to_purchase.lower() == 'n':
        runner()

    else:
        print("\nError: Invalid input. Please try again.")
        run_complete_order()


def clear_menu():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def runner():
    clear_menu()
    global current_customer_id
    if current_customer_id is not None:
        current_customer = bangazon.get_customer_per_customer_id(current_customer_id)
        print('\n Current User: ' + current_customer)
    print('\n Input option number:')
    print(generate_main_menu())
    user_input = input('\n > ')
    if user_input == '1':
        run_create_user()
        # runner()
    elif user_input == '2':
        run_select_user()
        # runner()
    elif user_input == '3':
        run_create_payment()
        # runner()
    elif user_input == '4':
        run_select_unpaid_order(True)
        # runner()
    elif user_input == '5':
        run_select_unpaid_order()
        # runner()
    elif user_input == '6':
        print(line_item_report.generate_product_popularity_report())
        # runner()
    elif user_input == '7':
        exit()


if __name__ == '__main__':
    runner()
