import unittest
from CountingBloomFilter import CountingBloomFilter

class TestCountingBloomFilter(unittest.TestCase):
    def testAddOne(self):
        test = CountingBloomFilter(10, 0.2)
        self.assertFalse(test.query('hello'))
        test.add('hello')
        self.assertTrue(test.query('hello'))
    
    def testAddTwo(self):
        test = CountingBloomFilter(10, 0.2)
        self.assertFalse(test.query('hello'))
        test.add('hello')
        test.add('ASDFAFJSDLGSDJFKLWEJGLWEF')
        self.assertTrue(test.query('hello'))
        self.assertTrue(test.query('ASDFAFJSDLGSDJFKLWEJGLWEF'))
        self.assertFalse(test.query('ASDFAFJSDLGSDJFKLWEJGLWE'))

    def testRemoveOne(self):
        test = CountingBloomFilter(10, 0.2)
        test.add('hello')
        self.assertTrue(test.query('hello'))
        test.remove('hello')
        self.assertFalse(test.query('hello'))
    
    def testRemoveTwo(self):
        test = CountingBloomFilter(10, 0.2)
        test.add('hello')
        test.add('ASDFAFJSDLGSDJFKLWEJGLWEF')
        test.remove('hello')
        self.assertFalse(test.query('hello'))
        self.assertTrue(test.query('ASDFAFJSDLGSDJFKLWEJGLWEF'))
        test.remove('ASDFAFJSDLGSDJFKLWEJGLWEF')
        self.assertFalse(test.query('ASDFAFJSDLGSDJFKLWEJGLWEF'))

if __name__ == '__main__':
    unittest.main()