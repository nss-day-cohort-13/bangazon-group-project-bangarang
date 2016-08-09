import bangazon
import customer_class

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
    user_input = int(input('\n >'))
    current_customer = stored_customers[stored_customers_list[user_input - 1]]

def runner():
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
        run_add_products()
    elif user_input == '5':
        run_complete_order()
    elif user_input == '6':
        run_generate_popularity_report()
    elif user_input == '7':
        pass

if __name__ == '__main__':
    runner()
