import bangazon

def generate_order_line_items_dictionary():
    '''
    Generate report dictionary from serialized order line items
    '''

    ## Declare main report dictionary
    report = dict()

    ## Deserialize stored dictionaries
    stored_order_line_items = bangazon.deserialize('order_line_items.txt')
    stored_products = bangazon.deserialize('products.txt')
    stored_orders = bangazon.deserialize('orders.txt')

    ## Iterate over key/value pairs in the stored_order_line_items dictionary
    ## Count instances of a given product_id, aggregate total revenue...
    ## and record unique customer ids
    for order_line_key in stored_order_line_items:

        ## Declare variable for order line item order object
        ## Use object and product id key properties...
        ## to reference objects in the stored orders and products dictionaries
        order_line_object = stored_order_line_items[order_line_key]
        product_object = stored_products[order_line_object.product_id]
        order_object = stored_orders[order_line_object.order_id]

        ## Check if product name is already a key in the report dictionary
        if dict.__contains__(report, product_object.name):

            ## Declare variables for pre-existing...
            ## order count, customer id set and revnue
            order_count = report[product_object.name]['order_count']
            revenue = report[product_object.name]['revenue']
            customer_id_set = report[product_object.name]['customer_id_set']

        ## Initialize order count and customer id set...
        # for new report dictionary keys
        else:
            order_count = 0
            revenue = 0
            customer_id_set = set()

        ## Increases product order count and stores unique customer ids in..
        ## customer id set and updates report dictionary
        order_count += 1
        revenue += float(product_object.price.replace(',','')[1:])
        customer_id_set.add(order_object.customer_id)
        report.update({product_object.name: {'order_count': order_count,
        'revenue': revenue, 'customer_id_set': customer_id_set,
        'customer_count': len(customer_id_set)}})

    return report

def generate_product_popularity_report():
    '''
    Generate string output for report dictionary
    '''

    ## Generate report dictionary from order line items
    report = generate_order_line_items_dictionary()

    ## Output header
    output = ('\n Product           Orders     Customers  Revenue\n' +
    ' *******************************************************\n')

    ## Iterate through report dictionary and format values for output
    for report_product_name in report:

        ## Declare variable for dictionaries associated...
        ## with report dictionary keys
        report_product_dict = report[report_product_name]

        ## Product name
        product_row += ((report_product_name[:14] + '... ')
        if len(report_product_name) > 17
        else report_product_name.ljust(18))

        ## Order count
        product_row += ((report_product_dict['order_count'][:7] + '... ')
        if len(str(report_product_dict['order_count'])) > 10
        else str(report_product_dict['order_count']).ljust(11))

        ## Customer count
        product_row += ((report_product_dict['customer_count'][:7] + '... ')
        if len(str(report_product_dict['customer_count'])) > 10
        else str(report_product_dict['customer_count']).ljust(11))

        ## Revenue
        product_row += ((report_product_dict['revenue'][:11] + '... ')
        if len(str(report_product_dict['revenue'])) > 14
        else str(report_product_dict['revenue']).ljust(15))

        ## Appends new product row to output
        output += (' ' + product_row + '\n')

    ## Output footer
    output += ' *******************************************************\n\n'

    return output
