import math
import random
import numpy

class MinHash():
    def __init__(self):
        # Use Tabulation Hashing to produce individual hash values
        # choose four random 8 bit tables
        self.t1 = [random.randint(0, 2**32 - 1) for _ in range(2**8)]
        self.t2 = [random.randint(0, 2**32 - 1) for _ in range(2**8)]
        self.t3 = [random.randint(0, 2**32 - 1) for _ in range(2**8)]
        self.t4 = [random.randint(0, 2**32 - 1) for _ in range(2**8)]

    def intern_hash(self, x):
        return self.t1[(x >> 24) & 0xff] ^ self.t2[(x >> 16) & 0xff ] ^\
            self.t3[(x >> 8) & 0xff] ^ self.t4[x & 0xff]

    def hash(self, L):
        return min([ self.intern_hash(x) for x in L])

    def get_element(self, L):
        h = self.hash(L)
        for x in L:
            if self.intern_hash(x) == h:
                return x

class OneBitMinHash():
    def __init__(self):
        self.h = MinHash()

    def hash(self, L):
        return self.h.hash(L) % 2


class BucketHashing():
    def __init__(self, universe_size, buckets, eps):
        assert universe_size % buckets == 0
        self.universe_size = universe_size
        self.buckets = buckets
        self.eps = eps
        self.h = MinHash()
        self.bucket_id = {}
        self.threshold = (self.buckets - 1) / (math.exp(self.eps) + self.buckets - 1)

        l = list(range(universe_size))
        random.shuffle(l)
        m = universe_size // buckets
        for i, x in enumerate(l):
            self.bucket_id[x] = i // m

    def hash(self, L):
        x = self.h.get_element(L)
        bucket = self.bucket_id[x]
        if random.random() <= self.threshold:
            return random.choice([i for i in range(self.buckets) if i != bucket])
        return bucket

class NoisyMinHash():
    def __init__(self, scale):
        self.h = OneBitMinHash()
        self.scale = scale

    def hash(self, L):
        return self.h.hash(L) + numpy.random.laplace(scale=self.scale)







