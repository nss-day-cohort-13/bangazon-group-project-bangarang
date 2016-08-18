import bangazon
import customer_class
import order_class
import payment_options_class
import order_line_item_class
import line_item_report
import order_line_item_class
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

# def run_create_user():
#     '''
#     Creates a new customer,
#     sets the current_user to be the new customer,
#     updates serialized customer dictionary
#     '''
#     global current_customer
#     clear_menu()
#     name = input('\n Name: ')
#     address = input('\n Address: ')
#     city = input('\n City: ')
#     state = input('\n State: ')
#     zip_code = input('\n Zip Code: ')
#     phone = input('\n Phone: ')
#     new_customer = customer_class.Customer(name, address, city, state, zip_code, phone)
#     bangazon.update_serialized_data('customers.txt', new_customer)
#     current_customer = new_customer
#     runner()

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

# def run_select_user():
#     '''
#     Displays list of customer names,
#     gets user input to select customer
#     and sets global current_customer
#     '''
#     global current_customer
#     clear_menu()
#     stored_customers = bangazon.deserialize('customers.txt')
#     stored_customers_list = list()
#     print('Select User:')
#     for key, customer_id in enumerate(stored_customers):
#         customer = stored_customers[customer_id]
#         stored_customers_list.append(customer.obj_id)
#         print('\n {0}. {1}'.format(key + 1, customer.name))
#     user_input = int(input('\n > '))
#     current_customer = stored_customers[stored_customers_list[user_input - 1]]
#     # print('\n Welcome {0}'.format(current_customer.name))
#     runner()

def run_select_user():
    '''
    Displays list of customer names,
    gets user input to select customer
    and sets global current_customer
    '''
    global current_customer_id
    clear_menu()
    stored_customers = bangazon.get_all_customers()
    for number, customer in enumerate(stored_customers, start=1):
        print(str(number) + ".) " + customer[1])
    choice = int(input('Who do you choose > '))
    current_customer_id = stored_customers[choice - 1][0]
    runner()

def run_create_payment():
    '''
    Deserialize stored payment dictionary,
    create new payment option from user input,
    and update serialized payment dictionary
    '''
    global current_customer
    global current_customer_id
    clear_menu()
    print(' Enter payment information below:')
    name = input(' Name: ')
    account_number = input(' Card Number: ')
    new_payment_option = payment_options_class.PaymentOption(name,
                         account_number, current_customer.obj_id)
    current_customer.payment_option_ids.append(new_payment_option.obj_id)
    print(bangazon.create_new_payment_option())
    runner()

    # global current_customer
    # clear_menu()
    # stored_payments = bangazon.deserialize('payments.txt')
    # stored_payments_list = list()
    # print(' Enter payment information below:')
    # name = input(' Name: ')
    # account_number = input(' Card Number: ')
    # new_payment_option = payment_options_class.PaymentOption(name, account_number, current_customer.obj_id)
    # current_customer.payment_option_ids.append(new_payment_option.obj_id)
    # bangazon.update_serialized_data('customers.txt', current_customer)
    # bangazon.update_serialized_data('payments.txt', new_payment_option)
    # runner()


def run_select_unpaid_order(add_products_menu=False):
    """ Displays all unpaid orders for the user that is currently logged in,
    and allows them to select which one they want. Will call the method to add products to
    an order if the add_products_menu is True, or will call the method to finalize an order.

    Method arguments:
    -----------------
    add_products_menu(boolean) -- When True, displays the option to create a new order, then calls the
                                 run_add_products method after user selection.
                                 If false, calls the run_complete_order method.
                                 Defaults to False.
    """
    global current_customer_id
    global current_order_id

    clear_menu()

    products_in_orders = bangazon.get_product_names_per_order_for_current_user(current_customer_id)
    print('POI', products_in_orders)
    for key, order in enumerate(products_in_orders):
        print('\n {0}. {1}'.format(key + 1, order[1]))

    if add_products_menu:

        print('\n 100. Start New Order')

    print('\n 0. Cancel')

    try:
        user_input = int(input(' > '))
    except ValueError:
        print("\nError: Incorrect input. Please try again.")
        run_select_unpaid_order()

    # what actions to perform based on user input
    if user_input == 0:
        runner()

    elif add_products_menu and user_input == 100:
        current_order_id = bangazon.create_new_order(current_customer_id)

    else:
        current_order_id = products_in_orders[user_input - 1][0]

    # calls next menu based on add_products_menu
    if add_products_menu:
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
        print("\nError: Incorrect input. Please try again.")
        run_add_products()

    # what actions to perform based on user input
    if user_input == 0:
        runner()

    else:
        selected_product_id = products[user_input - 1][0]

        bangazon.create_new_order_line_item(current_order_id,
                                            selected_product_id)
        run_add_products()


    # else:
    #     try:
    #         # gets the product selcted by the user and creates an
    #         # order line item with it's id and the current order id
    #         selected_product = stored_products_list[user_input - 1]
    #         new_order_line_item = order_line_item_class.OrderLineItem(current_order.obj_id, selected_product.obj_id)
    #         bangazon.update_serialized_data('order_line_items.txt', new_order_line_item)

    #     except IndexError:
    #         print("\nError: Input must be an integer in the range of options.")

    #     run_add_products()



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
        # all_payment_options = bangazon.deserialize('payments.txt')

###################sql database fetch###############################
        print()

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

def clear_menu():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def runner():
    clear_menu()
    global current_customer_id
    if current_customer_id != None:
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
