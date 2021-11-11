import math
import hashlib

""" Implementation of a Counting Bloom Filter """
class CountingBloomFilter:
    """ Initialize input size, false positive rate, bloom filter size, hash functions, and bloom filter """
    def __init__(self, n, p):
        # get input size and false positive rate
        self.inputSize = n
        self.falsePositive = p

        # from n and p, get the size of the counting bloom filter
        self.bloomSize = round(float(self.inputSize * math.log(1.0 / self.falsePositive)) / (math.log(2.0)) ** 2)
        # get number of hash functions (minimum of the ideal number of hash functions and the numbero of hash functions available in hashlib)
        self.numHash = min(round(float(self.bloomSize) * math.log(2.0) / self.inputSize), len(hashlib.algorithms_guaranteed))
        # get list of hash functions
        self.hashFunctions = list(hashlib.algorithms_guaranteed)[:self.numHash]

        # initialize bloom filter
        self.bloomFilter = [0] * self.bloomSize
    
    """ Hash element using k hash functions. Perform modulo by bloom filter size. Return list of keys """
    def hash(self, e):
        keys = []
        for fn in self.hashFunctions:
            h = hashlib.new(fn)
            h.update(e.encode())
            keys.append(int(h.hexdigest(), 16) % self.bloomSize)
        return keys
    
    """ Add element to counting bloom filter by hashing and incrementing count at filter index """
    def add(self, e):
        keys = self.hash(e)
        for key in keys:
            self.bloomFilter[key] += 1
    
    """ Look for an element in the counting bloom filter. Return True if found, False if not """
    def query(self, e):
        keys = self.hash(e)
        for key in keys:
            if self.bloomFilter[key] == 0:
                return False
        return True
    
    """ Remove an element from the counting bloom filter. Raise value error if element not found """
    def remove(self, e):
        keys = self.hash(e)
        if not self.query(e):
            raise ValueError("Element does not exist")
        for key in keys:
            self.bloomFilter[key] -= 1