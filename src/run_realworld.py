import yaml
import sys
import pickle
import random
from dataset_reader import read_data
from helpers import estimate_bucket_prob,\
    eps_minhash_bucket_conversion, eps_minhash_noisy_bucket_conversion,\
    estimate_noisy_bucket_minhash, estimate_jaccard_onebitminhash
from minhash import BucketHashing, NoisyMinHashBuckets, OneBitMinHash
from itertools import product
from multiprocessing import Pool
from math import ceil
import numpy


def to_set(X):
    Y = [set(x) for x in X.values()]
    return Y


def bruteforce(q, X, hashes, k=100):
    query = X[q]
    distances = []
    for i, p in enumerate(X):
        distances.append((i, estimate_noisy_bucket_minhash(
            query, p, hashes[0].buckets, hashes[0].scale)))
    return sorted(distances, key=lambda x: -x[1])[:k]


def run_experiment(input_tuple):
    name, k, eps, delta, b, dataset_info, seed = input_tuple
    numpy.random.seed(seed)
    random.seed(seed)
    ds_name, dataset, queries = dataset_info
    U = max([max(x) for x in dataset]) + 1
    res = []
    for run in RUNS:
        if name == "noisybucket":
            scale = eps_minhash_noisy_bucket_conversion(
                eps, tau, k, delta, b) / eps
            hashes = [NoisyMinHashBuckets(U, b, scale) for _ in range(k)]
        if name == "bucket":
            tt = ceil(eps_minhash_bucket_conversion(eps, tau, k, delta, b))
            hashes = [BucketHashing(U, b, eps / tt) for _ in range(k)]
        if name == "onebit":
            hashes = [OneBitMinHash() for _ in range(k)]

        # make dataset private
        if name == 'noisybucket':
            dist_f = lambda x, y: estimate_noisy_bucket_minhash(  # noqa: E731
                x, y, b, scale)
        if name == 'bucket':
            dist_f = lambda x, y: estimate_bucket_prob(  # noqa: E731
                x, y, 1 - hashes[0].threshold, b)
        if name == "onebit":
            dist_f = lambda x, y: estimate_jaccard_onebitminhash(x, y) # noqa: E731

        private_dataset = []
        for x in dataset:
            private_dataset.append([h.hash(x) for h in hashes])

        # perform queries on private dataset
        for q in queries:
            query = private_dataset[q]
            distances = []
            for i, p in enumerate(private_dataset):
                distances.append((i, dist_f(query, p)))
            res.append([run,
                        (q, [i for i, _ in sorted(distances, key=lambda x: -x[1])[:100]])])  # noqa: E501
    return {
        "name": name,
        "dataset_name": ds_name,
        "eps": eps,
        "buckets": b,
        "k": k,
        "results": res}


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('Usage: ./%s <yaml> [THREADS]' % sys.argv[0])
        sys.exit(1)
    f = open(sys.argv[1])
    exp_file = yaml.load(f)
    f.close()

    tasks = []

    global_params = exp_file['global']

    for task in global_params:
        KS = list(range(task['k']['min'],
                        task['k']['max'], task['k']['inc']))
        EPS = task['eps']
        DELTAS = task['delta']

        datasets = []
        querysets = []

        for name in task['datasets']:
            with open(name, 'rb') as f:
                queries, _, attributes = pickle.load(f)

            dataset_name = attributes["ds"]
            tau = attributes["tau"]

            dataset = to_set(read_data(dataset_name))
            new_dataset = []
            for x in dataset:
                if len(x) >= tau:
                    new_dataset.append(x)

            datasets.append((name, new_dataset, queries))

        experiments = exp_file['experiments']
        for e in experiments:
            if e['name'] == "noisybucket":
                tasks.extend(product(["noisybucket"], KS,
                                     EPS, DELTAS, e['b'], datasets))
            if e['name'] == "bucket":
                tasks.extend(product(["bucket"], KS, EPS,
                                     DELTAS, e['b'], datasets))
            if e['name'] == "onebit":
                tasks.extend(product(["onebit"], KS, [None],
                                     [None], [None], datasets))

    THREADS = 1
    if len(sys.argv) == 3:
        THREADS = int(sys.argv[2])
    SEED = exp_file['environment']['seed']
    RUNS = list(range(exp_file['environment']['runs']))

    tasks_with_seeds = []

    for i, t in enumerate(tasks):
        tasks_with_seeds.append((*t, SEED + i))


#    print(tasks_with_seeds)
    pool = Pool(processes=THREADS)
    results = pool.map(run_experiment, tasks_with_seeds)
    pool.close()
    pool.join()

    fn = sys.argv[1].split("/")[-1].split(".")[0] + ".results.pickle"
    with open(fn, 'wb') as f:
        pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)
