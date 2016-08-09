import unittest
from product import *
class TestProduct(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        """ sets up product for all tests"""
        self.product = Product('macbook pro', '$1200')

    def test_product_name_value(self):
        """ asserts that self.product.name is equal to 'macbook pro'"""
        self.assertEqual(self.product.name, 'macbook pro')

    def test_product_price_value(self):
        """ asserts that self.product.name is equal to '$1200'"""
        self.assertEqual(self.product.price, '$1200')

    def test_product_id_is_not_none(self):
        """ asserts that self.product.id is not None"""
        self.assertIsNotNone(self.product.obj_id)

if __name__ == '__main__':
    unittest.main()
