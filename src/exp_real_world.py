from dataset_reader import read_data
from helpers import *
from minhash import *
from datetime import datetime

import sys

datasets = {
        "lastfm" : read_data("lastfm.dat"),
        "movielens" : read_data("movielens.dat")
}

RUNS = list(range(5))
#KS = list(range(5, 30, 5))

dataset = sys.argv[1]
if dataset not in datasets:
    print("Cannot find dataset")
    exit(-1)

method = sys.argv[2]

KS = [int(sys.argv[3])]

if method == 'bucket':
    eps = int(sys.argv[4])
    bf = float(sys.argv[5])

def experiment(hashes, estimation, data, experiment_pairs):
    hashed_data = {}
    for x in data:
        hashed_data[x] = [h.hash(data[x]) for h in hashes]
    for x, y in experiment_pairs:
        yield (jaccard(data[x],data[y]), estimation(hashed_data[x], hashed_data[y]))

data = datasets[dataset]
experiment_pairs = []
universe_size = max([max(data[x]) for x in data]) + 2

for x in data:
    for y in data:
        if jaccard(data[x], data[y]) > 0.2:
            experiment_pairs.append((x,y))

for K in KS:
    for run in RUNS:
        if method == 'noisy':
            minhashes = [MinHash() for _ in range(K)]
            onebitminhashes = [OneBitMinHash() for _ in range(K)]

            #for t,e in experiment(minhashes, estimate_jaccard_minhash, data, experiment_pairs):
            #    print("minhash", datetime.now(), dataset, K, t, e, run, sep=',')

            #for t, e in experiment(onebitminhashes, estimate_jaccard_onebitminhash, data, experiment_pairs):
            #    print("onebit", datetime.now(), dataset, K, t, e, run, sep=',')

            for scale in [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35]:
                noisyminhashes = [NoisyMinHash(scale) for _ in range(K)]
                for t, e in experiment(noisyminhashes, lambda L1, L2: estimate_noisy_minhash(L1, L2, scale), data, experiment_pairs):
                    print("noisy", datetime.now(), dataset, K, t, e, scale, run, sep=",")
        if method == 'bucket':
            b = int(bf * universe_size)
            while universe_size % b != 0:
                b += 1
            buckethashes = [BucketHashing(universe_size, b, eps) for _ in range(K)]
            for t, e in  experiment(buckethashes, lambda L1, L2: estimate_bucket_prob(L1, L2, 1 - buckethashes[0].threshold, b), data, experiment_pairs):
                print("bucket", datetime.now(), dataset, K, t, e, bf, b, eps, run, sep=',')





