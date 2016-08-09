def create_product():
    all_products = deserialize('products.txt')
    product_name = input('what is the product name? > ')
    product_price = input('what is the product price? > ')
    newProduct = Product(product_name, product_price)
    all_products[newProduct.product_id] = newProduct
    products_final = serialize('products.txt', all_products)
    return products finally

if __name__ == '__main__':
    create_product()
