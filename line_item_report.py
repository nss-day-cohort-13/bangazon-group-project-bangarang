import bangazon
def generate_order_line_items_report():
    '''generates report from line items.'''
    stored_order_line_items = bangazon.deserialize('order_line_items.txt')
    stored_products = bangazon.deserialize('products.txt')
    stored_orders = bangazon.deserialize('orders.txt')
    order_report = dict()
    customer_report = dict()

    for order_line_key in stored_order_line_items:
        order_line_object = stored_order_line_items[order_line_key]
        product_object = stored_products[order_line_object.obj_id]
        order_object = stored_orders[order_line_object.order_id]

        try:
            product_count = order_report[product_object.name]
            customer_report[product_object.name].add(product_object.customer_id)
        except:
            customer_report.update({product_object.name: {order_object.customer_id}})
            product_count = 0

        product_count += 1
        order_report.update({product_object.name: product_count})
