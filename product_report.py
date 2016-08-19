import locale
import bangazon

def generate_product_report():
'''
Generate report dictionary from stored order line items
'''

    ## Declare main report dictionary...
    ## and get stored line items from database
    report = dict()
    stored_order_line_items = bangazon.get_all_order_line_items()

    ## Iterate through list of stored_line_items tuples
    for line_item in stored_order_line_items:

        ## Initialize variables for order and product ids
        order_id = line_item[1]
        product_id = line_item[2]

        ## Get order data for current product...
        ## and declare variable for paid in full status
        order_tuple = bangazon.get_order_per_order_id(order_id)
        order_paid_in_full = order_tuple[3]

        ## Check that order has been paid for
        if order_paid_in_full == 1:

            ## Get product data for current product...
            ## and initialize variables for product's name and price
            product_tuple = bangazon.get_product_per_product_id(product_id)
            product_name = product_tuple[1]
            product_price = int(product_tuple[2])

            ## Check for existing product entry in report dictionary...
            ## and set report variables to current values
            if dict.__contains__(report, product_name):
                order_count = report[product_name]['order_count']
                revenue = report[product_name]['revenue']
                customer_id_set = report[product_name]['customer_id_set']

            ## Initialize report variables for new report dictionary entries
            else:
                order_count = 0
                revenue = 0
                customer_id_set = set()

            ## Increment report variable values
            order_count += 1
            revenue += product_price
            customer_id_set.add(order_tuple[2])

            ## Update report products entry in report dictionary
            report.update({product_name: {'order_count': order_count,
            'revenue': revenue, 'customer_id_set': customer_id_set,
            'customer_count': len(customer_id_set)}})

    return report

def generate_order_totals_dictionary(report):
    '''
    Generates total orders, customers, and revenue for product popularity report
    '''

    ## Initialize totals variables
    total_orders = 0
    total_customers = 0
    total_revenue = 0

    ## Iterates through products in report dictionary...
    ## and aggregates total values
    for product_name in report:
        report_product_dictionary = report[product_name]
        total_orders += report_product_dictionary['order_count']
        total_customers += report_product_dictionary['customer_count']
        total_revenue += report_product_dictionary['revenue']

    return { 'total_orders': total_orders, 'total_customers': total_customers,
    'total_revenue': total_revenue}

def generate_product_popularity_report():
    '''
    Generate string output for report dictionary
    '''
    ## Sets locale for currency formatting
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    ## Generate report dictionary from order line items
    report = generate_product_report()

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
        product_row += ((locale.currency(report_product_dict['revenue'],
        grouping = True)[:11] + '... ')
        if len(str(report_product_dict['revenue'])) > 14
        else locale.currency(report_product_dict['revenue'],
        grouping = True).ljust(15))

        ## Appends new product row to output
        output += (' ' + product_row + '\n')

    output += ' *******************************************************\n'

    ## Totals row
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
    totals_row += ((locale.currency(total_revenue,
    grouping = True)[:11] + '... ')
    if len(str(total_revenue)) > 14
    else locale.currency(total_revenue, grouping = True).ljust(15))

    ## Appends totals row to output
    output += (' ' + totals_row + '\n')

    return output
