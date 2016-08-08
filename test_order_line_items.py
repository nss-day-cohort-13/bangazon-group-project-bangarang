import unittest
from order_line_items import *


class TestOrderLineItem(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.oli = OrderLineItem(123456789, 987654321)

    def test_create_order_line_item(self):
        self.assertEqual(self.oli.order_id, 123456789)
        self.assertEqual(self.oli.product_id, 987654321)
        self.assertIsInstance(self.oli.order_line_item_id, int)


if __name__ == '__main__':
    unittest.main()
