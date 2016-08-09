from bangazon import *
def generate_main_menu():
    output = '\n 1. Create A Customer Account' +
    '\n 3. Create A Payment Option' +
    '\n 4. Add Product To Shopping Cart' +
    '\n 5. Complete An Order' +
    '\n 6. See Product Popularity' +
    '\n 7. Leave Bangazon'
    return output


def runner():
    print(generate_main_menu())
    print('\n Input option number:')
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
