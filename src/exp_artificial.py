from data_generator import *
from helpers import *
from minhash import *
from datetime import datetime
import sys

DS = [20, 50, 100, 200, 500]

KS = list(range(5, 105, 5))

RUNS = list(range(20))


def experiment(hashes, estimation, X, other_data):
    X_hashes = [h.hash(X) for h in hashes]
    for Y in other_data:
        Y_hashes = [h.hash(Y) for h in hashes]
        yield (jaccard(X,Y), estimation(X_hashes, Y_hashes))

def bucket_experiment(X, other_data, D, K):
    if K >= 30:
        return
    usize = 2 * (max(X) + 2) # largest element in the list
    sparsities = [1.0, 2.0, 5.0, 10.0, 50.0]
    bucket_factors = [0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0]
    eps_vals = [0.25, .5, 1, 2, 4, 6, 8, 10, 12, 14, 16]
    for run in RUNS:
        for bf in bucket_factors:
            for s in sparsities:
                for eps in eps_vals:
                    U = int(usize * s)
                    b = int(bf * U)
                    while U % b != 0:
                        b += 1
                    buckethashes = [BucketHashing(U, b, eps) for _ in range(K)]
                    for t, e in  experiment(buckethashes, lambda L1, L2: estimate_bucket_prob(L1, L2, 1 - buckethashes[0].threshold, b), X, other_data):
                        print("bucket", datetime.now(), D, K, t, e, bf, b, s, eps, run, sep=',')

for D in DS:
    X = generate_items(D)
    data = [produce_pair(X, eps / 20) for eps in range(20)]

    for K in KS:
        for run in RUNS:
            minhashes = [MinHash() for _ in range(K)]
            onebitminhashes = [OneBitMinHash() for _ in range(K)]

            for t, e in experiment(minhashes, estimate_jaccard_minhash, X, data):
                print("minhash", datetime.now(), D, K, t, e, run, sep=',')

            for t, e in experiment(onebitminhashes, estimate_jaccard_onebitminhash, X, data):
                print("onebit", datetime.now(), D, K, t, e, run, sep=',')

            for scale in [i / 20 for i in range(21)]:
                noisyminhashes = [NoisyMinHash(scale) for _ in range(K)]
                for t, e in experiment(noisyminhashes, lambda L1, L2: estimate_noisy_minhash(L1, L2, scale), X, data):
                    print("noisy", datetime.now(), D, K, t, e, scale, run, sep=",")

        bucket_experiment(X, data, D, K)



