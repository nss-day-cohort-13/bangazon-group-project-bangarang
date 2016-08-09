import unittest
from customer_class import *


class TestCustomer(unittest.TestCase):
    '''Set up and test a new customer'''

    @classmethod
    def setUpClass(self):
        self.customer = Customer('Mike Mead',
                                 'yourmomshouse',
                                 'nashville',
                                 'TN',
                                 37075,
                                 '615-200-1919')

    def test_create_customer(self):
        self.assertEqual(self.customer.name, 'Mike Mead')
        self.assertEqual(self.customer.address, 'yourmomshouse')
        self.assertEqual(self.customer.city, 'nashville')
        self.assertEqual(self.customer.state, 'TN')
        self.assertEqual(self.customer.zip_code, 37075)
        self.assertEqual(self.customer.phone, '615-200-1919')
        self.assertIsNotNone(self.customer.obj_id)


if __name__ == '__main__':
    unittest.main()
