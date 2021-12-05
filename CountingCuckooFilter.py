from abc import abstractmethod
import math
import mmh3
from bitarray import bitarray
import codecs
from bucket import Bucket
import random

class CuckooTemplate():

    DEFAULT_ERROR_RATE = 0.0001

    def __init__(self, capacity, error_rate, bucket_size=4, max_kicks=500):
        self.capacity = capacity
        self.bucket_size = bucket_size
        self.max_kicks = max_kicks
        if error_rate:
            self.error_rate = error_rate
        else:
            self.error_rate = CuckooFilter.DEFAULT_ERROR_RATE
        min_fp = math.log(1.0/self.error_rate, 2) + math.log(2*self.bucket_size, 2)
        self.fingerprint_size = int(math.ceil(min_fp))
        self.size = 0

    @abstractmethod
    def insert(self, item):
        pass

    @abstractmethod
    def lookup(self, item):
        pass

    @abstractmethod
    def delete(self, item):
        pass

    def fingerprint(self, item):
        # truncate Murmur hashing to fingerprint size
        mmh3_hash = bitarray()
        mmh3_hash.frombytes(mmh3.hash_bytes(item))
        return mmh3_hash[:self.fingerprint_size]

    def index(self, item):
        item_hash = mmh3.hash_bytes(item)
        return int(codecs.encode(item_hash, 'hex'), 16) % self.capacity

    def indices(self, item, fingerprint):
        index = self.index(item)
        indices = [index]
        # partial-key Cuckoo hashing
        h_value = (index ^ self.index(fingerprint.tobytes())) % self.capacity
        indices.append(h_value)
        for index in indices:
            yield index

    def load_factor(self):
        return round(float(self.size) / (self.capacity * self.bucket_size), 4)


class CuckooFilter(CuckooTemplate):
    def __init__(self, capacity, error_rate, bucket_size=4, max_kicks=500):
        super(CuckooFilter, self).__init__(capacity, error_rate, bucket_size, max_kicks)
        self.buckets = [None] * self.capacity

    def insert(self, item):
        fingerprint = self.fingerprint(item)
        indices = []
        for index in self.indices(item, fingerprint):
            indices.append(index)
            if self.buckets[index] is None:
                self.buckets[index] = Bucket(size=self.bucket_size)
            if self.buckets[index].insert(fingerprint):
                self.size =+ 1
                return index
        # all available buckets full
        index = random.choice(indices)
        orig_index = index
        curr_pair = (fingerprint, 1)
        #pair_stack = [curr_pair]
        #index_stack = [index]
        for _ in range(self.max_kicks):
            curr_pair = self.buckets[index].swap(curr_pair)
            #pair_stack.append(curr_pair)
            fingerprint = curr_pair[0]
            index = (index ^ self.index(fingerprint.tobytes())) % self.capacity
            #index_stack.append(index)
            if self.buckets[index] is None:
                # initialize bucket if needed
                self.buckets[index] = Bucket(size=self.bucket_size)
            if self.buckets[index].insert_pair(curr_pair):
                self.size += 1
                return orig_index
            
        # len(pair_stack) should = len(index_stack)
        # reaching full capacity, need to rewind pair_stack and restore them, NOT HANDELED THIS TIME

    def lookup(self, item):
        fingerprint = self.fingerprint(item)
        for index in self.indices(item, fingerprint):
            if self.buckets[index] is None:
                self.buckets[index] = Bucket(size=self.bucket_size)
            if self.buckets[index].contains(fingerprint):
                return True
        return False

    def delete(self, item):
        fingerprint = self.fingerprint(item)
        for index in self.indices(item, fingerprint):
            if self.buckets[index] is None:
                self.buckets[index] = Bucket(size=self.bucket_size)
            if self.buckets[index].delete(fingerprint):
                self.size -= 1
                return True
        return False