import bangazon
import locale

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
        if order_object.paid_in_full == True:

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

def generate_order_totals_dictionary(report):
    '''Generate order totals'''
    total_orders = 0
    total_customers = 0
    total_revenue = 0
    for product_name in report:
        report_product_dictionary = report[product_name]
        total_orders += report_product_dictionary['order_count']
        total_customers += report_product_dictionary['customer_count']
        total_revenue += report_product_dictionary['revenue']
    return { 'total_orders': total_orders, 'total_customers': total_customers, 'total_revenue': total_revenue}

def generate_product_popularity_report():
    '''
    Generate string output for report dictionary
    '''

    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    ## Generate report dictionary from order line items
    report = generate_order_line_items_dictionary()

    ## Generate totals from report dictionary
    report_totals_dict = generate_order_totals_dictionary(report)
    total_orders = report_totals_dict['total_orders']
    total_customers = report_totals_dict['total_customers']
    total_revenue = report_totals_dict['total_revenue']

    ## Output header
    output = ('\n Product           Orders     Customers  Revenue\n' +
    ' *******************************************************\n')

    ## Iterate through report dictionary and format values for output
    for report_product_name in report:

        ## Declare variable for dictionaries associated...
        ## with report dictionary keys
        report_product_dict = report[report_product_name]

        ## Product name
        product_row = ((report_product_name[:14] + '... ')
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
        product_row += ((locale.currency(report_product_dict['revenue'], grouping = True)[:11] + '... ')
        if len(str(report_product_dict['revenue'])) > 14
        else locale.currency(report_product_dict['revenue'], grouping = True).ljust(15))

        ## Appends new product row to output
        output += (' ' + product_row + '\n')

    output += ' *******************************************************\n'

    ## Product name
    totals_row = ('Totals:'.ljust(18))

    ## Order count
    totals_row += ((total_orders[:7] + '... ')
    if len(str(total_orders)) > 10
    else str(total_orders).ljust(11))

    ## Customer count
    totals_row += ((total_customers[:7] + '... ')
    if len(str(total_customers)) > 10
    else str(total_customers).ljust(11))

    ## Revenue
    totals_row += ((locale.currency(total_revenue, grouping = True)[:11] + '... ')
    if len(str(total_revenue)) > 14
    else locale.currency(total_revenue, grouping = True).ljust(15))

    ## Appends new product row to output
    output += (' ' + totals_row + '\n')

    ## Output footer

    return output
