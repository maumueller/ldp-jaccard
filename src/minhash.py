import math
import random
import numpy


class MinHash():
    def __init__(self):
        # choose four random 8 bit tables
        self.t1 = [random.randint(0, 2**32 - 1) for _ in range(2**8)]
        self.t2 = [random.randint(0, 2**32 - 1) for _ in range(2**8)]
        self.t3 = [random.randint(0, 2**32 - 1) for _ in range(2**8)]
        self.t4 = [random.randint(0, 2**32 - 1) for _ in range(2**8)]

    def intern_hash(self, x):
        return self.t1[(x >> 24) & 0xff] ^ self.t2[(x >> 16) & 0xff] ^\
            self.t3[(x >> 8) & 0xff] ^ self.t4[x & 0xff]

    def hash(self, L):
        return min([self.intern_hash(x) for x in L])

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
        self.universe_size = universe_size
        self.buckets = buckets
        self.eps = eps
        self.h = MinHash()
        self.bucket_id = {}
        self.threshold = (self.buckets - 1) / \
            (math.exp(self.eps) + self.buckets - 1)

        for x in range(universe_size):
            self.bucket_id[x] = random.choice(range(self.buckets))

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


class NoisyMinHashBuckets():
    def __init__(self, universe_size, buckets, scale):
        self.universe_size = universe_size
        self.buckets = buckets
        self.scale = scale
        self.h = MinHash()
        self.bucket_id = {}

        for x in range(universe_size):
            self.bucket_id[x] = random.choice(range(self.buckets))

    def hash(self, L):
        x = self.h.get_element(L)
        bucket = self.bucket_id[x]
        return bucket + numpy.random.laplace(scale=self.scale)


class RROneBitMinHash():
    def __init__(self, eps):
        self.h = OneBitMinHash()
        self.eps = eps
        self.threshold = 1 / (math.exp(eps) + 1)

    def hash(self, L):
        hv = self.h.hash(L)
        if random.random() <= self.threshold:
            return 1 - hv
        else:
            return hv
