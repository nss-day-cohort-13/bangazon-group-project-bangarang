import unittest
from bangazon import *
class TestSerialization(unittest.TestCase):
    def test_serialize_function_works(self):
        test_string = 'string'
        serialize('test_serialization.txt', test_string)
        with open('test_serialization.txt', 'rb+') as f:
            stored_string = pickle.load(f)
        self.assertEqual(test_string, stored_string)

    def test_deserialize_function_works(self):
        test_string = 'string'
        with open('test_serialization.txt', 'wb+') as f:
            pickle.dump(test_string, f)
        stored_string = deserialize('test_serialization.txt')
        self.assertEqual(test_string, stored_string)

if __name__ == '__main__':
    unittest.main()
