from data_generator import *
from helpers import *
from minhash import *

K = 50
D = 100

B = 5
U = 1000
EPS = 20

SCALE = 0.0

X = generate_items(D)
Y = produce_pair(X, .8)
Z = produce_pair(X, .5)
ZZ = produce_pair(X, .25)

minhashes = [MinHash() for _ in range(K)]
onebitminhashes = [OneBitMinHash() for _ in range(2 * K)]

def experiment(hashes, estimation):
    X_hashes = [h.hash(X) for h in hashes]
    Y_hashes = [h.hash(Y) for h in hashes]
    Z_hashes = [h.hash(Z) for h in hashes]
    ZZ_hashes = [h.hash(ZZ) for h in hashes]
    print('true:', jaccard(X, Y), 'estimated:', estimation(X_hashes, Y_hashes))
    print('true:', jaccard(X, Z), 'estimated:', estimation(X_hashes, Z_hashes))
    print('true:', jaccard(X, ZZ), 'estimated:', estimation(X_hashes, ZZ_hashes))


def bucket_experiment(B, U):
    eps = 0.5
    while eps < 32:
        buckethashes = [BucketHashing(U, B, eps) for _ in range(K)]
        print(eps)
        experiment(buckethashes, lambda L1, L2: estimate_bucket_prob(L1, L2, 1 - buckethashes[0].threshold, B))
        eps *= 2

experiment(minhashes, estimate_jaccard_minhash)
experiment(onebitminhashes, estimate_jaccard_onebitminhash)
for scale in [0.0, 0.25, 0.5, 1, 2]:
    noisyminhashes = [NoisyMinHash(scale) for _ in range(2 * K)]
    print("Experiments with added noise %f" % scale)
    experiment(noisyminhashes, lambda L1, L2: estimate_noisy_minhash(L1, L2, scale))
print("Bucket experiments:")
bucket_experiment(10, U)






