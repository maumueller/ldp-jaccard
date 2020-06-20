from helpers import jaccard
from dataset_reader import read_data
import random
import pickle
import sys


def to_set(X):
    Y = [set(x) for x in X.values()]
    return Y


def bruteforce(X):
    distances = {}
    for i, x in enumerate(X):
        for j, y in enumerate(X):
            distances.setdefault(i, []).append((j, jaccard(x, y)))

    for k in distances:
        distances[k].sort(key=lambda x: -x[1])

    return distances


def find_interesting_queries(X, query_id):
    distances = bruteforce(X)

    if query_id:
        return [query_id], distances
    else:
        interesting_queries = []

        for k in distances:
            if distances[k][10][1] > 0.2:
                interesting_queries.append(k)

        print(len(interesting_queries))

        random.shuffle(interesting_queries)
        return interesting_queries[:50], distances


if __name__ == '__main__':
    ds = sys.argv[1]
    tau = int(sys.argv[2])
    random.seed(12345)
    attributes = {
        "ds": ds,
        "tau": tau
    }
    query_id = None
    if len(sys.argv) == 4:
        query_id = int(sys.argv[3])
    dataset = to_set(read_data(ds))
    new_dataset = []
    for x in dataset:
        if len(x) >= tau:
            new_dataset.append(x)
    print(len(dataset))
    print(len(new_dataset))
    queries, ground_truth = find_interesting_queries(new_dataset, query_id)

    with open(ds + "." + str(tau) + '.pickle', 'wb') as f:
        pickle.dump([queries, ground_truth, attributes],
                    f, pickle.HIGHEST_PROTOCOL)
