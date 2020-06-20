import yaml
import sys
from minhash import NoisyMinHashBuckets, BucketHashing, OneBitMinHash
from data_generator import generate_items, produce_pair
from helpers import jaccard, eps_minhash_bucket_conversion, \
    estimate_noisy_bucket_minhash, estimate_bucket_prob, \
    eps_minhash_noisy_bucket_conversion, \
    estimate_jaccard_onebitminhash
from itertools import product
from datetime import datetime
from multiprocessing import Pool
from math import ceil
import random
import numpy

# TODO unify random and real world experiments


def experiment(hashes, estimation, X, other_data):
    X_hashes = [h.hash(X) for h in hashes]
    for Y in other_data:
        Y_hashes = [h.hash(Y) for h in hashes]
        yield (jaccard(X, Y), estimation(X_hashes, Y_hashes))


def run_experiment(input_tuple):
    res = []
    name, D, K, sim, eps, delta, b, seed = input_tuple
    numpy.random.seed(seed)
    random.seed(seed)
    X = generate_items(D)
    data = [produce_pair(X, sim)]
    U = max(X + data[0]) + 1
    for run in RUNS:
        if name == "noisybucket":
            scale = eps_minhash_noisy_bucket_conversion(
                eps, D, K, delta, b) / eps
            noisyminhashes = [NoisyMinHashBuckets(
                U, b, scale) for _ in range(K)]
            for t, e in experiment(noisyminhashes, lambda L1, L2: estimate_noisy_bucket_minhash(L1, L2, b, scale), X, data):  # noqa: E501
                res.append(["noisy_bucket", str(datetime.now()),
                            D, K, t, e, b, eps, run])
        if name == "bucket":
            tt = ceil(eps_minhash_bucket_conversion(eps, D, K, delta, b))
            buckethashes = [BucketHashing(U, b, eps / tt) for _ in range(K)]
            for t, e in experiment(buckethashes, lambda L1, L2: estimate_bucket_prob(L1, L2, 1 - buckethashes[0].threshold, b), X, data):  # noqa: E501
                res.append(["bucket", str(datetime.now()),
                            D, K, t, e, b, eps, run])
        if name == "onebit":
            hashes = [OneBitMinHash() for _ in range(K)]
            for t, e in experiment(hashes, lambda L1, L2:
                    estimate_jaccard_onebitminhash(L1, L2), X, data):  # noqa: E501
                res.append(["onebit", str(datetime.now()),
                            D, K, t, e, run])

    return res


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('Usage: ./%s <yaml> [THREADS]' % sys.argv[0])
        sys.exit(1)
    f = open(sys.argv[1])
    exp_file = yaml.load(f)
    f.close()

    tasks = []

    global_params = exp_file['global']

    SIM = global_params['threshold']
    DS = global_params['size']
    RUNS = list(range(global_params['runs']))
    KS = list(range(global_params['k']['min'],
                    global_params['k']['max'], global_params['k']['inc']))
    EPS = global_params['eps']
    DELTAS = global_params['delta']

    experiments = exp_file['experiments']
    for e in experiments:
        if e['name'] == 'noisy':
            tasks.extend(product(["noisy"], DS, KS, SIM, EPS, DELTAS, [None]))
        if e['name'] == "noisybucket":
            tasks.extend(product(["noisybucket"], DS,
                                 KS, SIM, EPS, DELTAS, e['b']))
        if e['name'] == "bucket":
            tasks.extend(product(["bucket"], DS, KS, SIM, EPS, DELTAS, e['b']))
        if e['name'] == "onebit":
            tasks.extend(product(["onebit"], DS, KS, SIM, [None], [None], [None]))

    THREADS = 1
    if len(sys.argv) == 3:
        THREADS = int(sys.argv[2])
    SEED = exp_file['environment']['seed']

    tasks_with_seeds = []

    for i, t in enumerate(tasks):
        tasks_with_seeds.append((*t, SEED + i))

    pool = Pool(processes=THREADS)
    results = pool.map(run_experiment, tasks_with_seeds)
    pool.close()
    pool.join()

    fn = sys.argv[1].split("/")[-1].split(".")[0] + ".csv"
    with open(fn, "w") as f:
        for res in results:
            for s in res:
                f.write(",".join(map(str, s)) + "\n")
