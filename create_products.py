import locale
from bangazon import *
from product import *
def create_product():
    locale.setlocale(locale.LC_ALL, 'en_US')
    all_products = deserialize('products.txt')
    product_name = input('what is the product name? > ')
    product_price = int(input('what is the product price? > '))
    format_product_price = locale.currency(product_price, grouping=True)
    newProduct = Product(product_name, format_product_price)
    all_products[newProduct.product_id] = newProduct
    serialize('products.txt', all_products)
    product_menu()

def product_menu():
    print('1. Create Product')
    print('2. Leave Creator')
    selection = input('What is your choice? > ')

    if int(selection) > 0 and int(selection) < 3:
        if int(selection) == 1:
            create_product()

if __name__ == '__main__':
    product_menu()
