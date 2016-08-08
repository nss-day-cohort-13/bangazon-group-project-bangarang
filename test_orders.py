import unittest
from orders import *


class TestOrders(unittest.TestCase):
    '''Set up and test a new order'''

    @classmethod
    def setUpClass(self):
        self.order = Orders(123333, 1212121212, True)

    def test_create_orders(self):
        self.assertIsInstance(self.order.order_id, int)
        self.assertEqual(self.order.payment_option_id, 123333)
        self.assertEqual(self.order.customer_id, 1212121212)
        self.assertEqual(self.order.paid_in_full, True)




if __name__ == '__main__':
    unittest.main()
