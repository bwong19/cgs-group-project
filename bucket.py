import random

class Bucket():
    def __init__(self, size=4):
        self.size = size
        self.bucket = []

    def is_full(self):
        return len(self.bucket) >= self.size

    def insert(self, fingerprint):
        for i in range(len(self.bucket)):
            if self.bucket[i][0] == fingerprint:
                occ = self.bucket[i][1]
                self.bucket[i] = (fingerprint, occ+1)
                return True
        if not self.is_full():
            self.bucket.append((fingerprint, 1))
            return True
        return False
    
    def contains(self, fingerprint):
        for i in range(len(self.bucket)):
            if self.bucket[i][0] == fingerprint:
                return True
        return False

    def delete(self, fingerprint):
        for i in range(len(self.bucket)):
            if self.bucket[i][0] == fingerprint:
                occ = self.bucket[i][1]
                if occ == 1:
                    self.bucket.remove(self.bucket[i])
                    return True
                else:
                    self.bucket[i] = (fingerprint, occ-1)
                    return True
        return False

    def swap(self, pair):
        rindex = random.choice([i for i in range(len(self.bucket))])
        kicked = self.bucket[rindex]
        self.bucket[rindex] = pair
        return kicked

    def insert_pair(self, pair):
        if not self.is_full():
            self.bucket.append(pair)
            return True
        return False