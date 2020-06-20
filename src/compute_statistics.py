import sys
import pickle
from dataset_reader import read_data
from helpers import jaccarddirect


def to_set(X):
    Y = [set(x) for x in X.values()]
    return Y


res_file = sys.argv[1]

with open(res_file, 'rb') as f:
    results = pickle.load(f)

# preload all datasets

dataset_names = set()


for res in results:
    dataset_names.add(res["dataset_name"])

distance_cache = {}

for name in dataset_names:
    with open(name, 'rb') as f:
        queries, distances, attributes = pickle.load(f)

    dataset_name = attributes["ds"]
    tau = attributes["tau"]

    dataset = to_set(read_data(dataset_name))
    new_dataset = []
    for x in dataset:
        if len(x) >= tau:
            new_dataset.append(x)
        distance_cache[name] = {
                "distances": distances,
                "dataset": new_dataset
                }


print("dsname", "algoname", "eps", "k", "buckets", "R@10", "R@50", "R@100",
      "Approx", sep=",")

cache = {}


def compute_distance(dataset, name, i, j):
    if (name, i, j) not in cache:
        cache[(name, i, j)] = jaccarddirect(dataset[i], dataset[j])
    return cache[(name, i, j)]


# compute how many of 1-NN are found in 100-NN
for res in results:
    ds_name = res["dataset_name"]
    distances = distance_cache[ds_name]["distances"]
    dataset = distance_cache[ds_name]["dataset"]
    n100 = 0
    n50 = 0
    n10 = 0
    total = 0
    origin_sim = 0
    approx_sim = 0
    for _, (q, neighbors) in res["results"]:
        total += 1
        for j, p in enumerate(neighbors[1:]):
            if p == q:
                continue
            if compute_distance(dataset, ds_name, p, q) >= \
                    distances[q][1][1] - 0.01:
                n100 += 1
                if j < 51:
                    n50 += 1
                if j < 11:
                    n10 += 1
                break

#        if distances[q][1][0] in neighbors:
#            n100 += 1
#        if distances[q][1][0] in neighbors[:11]:
#            n10 += 1
        for i in range(1, 11):
            origin_sim += distances[q][i][1]
        p_found = False
        for i in range(10):
            if neighbors[i] == q:
                p_found = True
            else:
                approx_sim += compute_distance(dataset, ds_name,
                                               neighbors[i], q)
        if p_found:
            approx_sim += compute_distance(dataset, ds_name, neighbors[10], q)

    print(res["dataset_name"], res["name"], res["eps"], res["k"],
          res["buckets"], n10 / total, n50 / total, n100 / total,
          approx_sim / origin_sim, sep=",")
