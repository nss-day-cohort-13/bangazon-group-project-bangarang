import unittest
from payment_options import *


class TestPayment(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.payment = PaymentOption("Visa", 123456789)

    def test_create_payment(self):
        self.assertEqual(self.payment.name, "Visa")
        self.assertEqual(self.payment.account_number, 123456789)
        self.assertIsNotNone(self.payment.payment_option_id)
        self.assertIsInstance(self.payment.payment_option_id, int)


if __name__ == '__main__':
    unittest.main()
