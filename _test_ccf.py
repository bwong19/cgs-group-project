import unittest
from bucket import Bucket
from CountingCuckooFilter import CuckooFilter

class TestCountingCuckooFilter(unittest.TestCase):
    def testAddOne(self):
        test = CuckooFilter(10, 0.1)
        self.assertFalse(test.lookup('hello'))
        test.insert('hello')
        self.assertTrue(test.lookup('hello'))

    def testAddTwo(self):
        test = CuckooFilter(10, 0.1)
        self.assertFalse(test.lookup('hello'))
        test.insert('hello')
        test.insert('ALKSERT')
        self.assertTrue(test.lookup('hello'))
        self.assertTrue(test.lookup('ALKSERT'))
        self.assertFalse(test.lookup('ALKSEET'))

if __name__ == '__main__':
    unittest.main()