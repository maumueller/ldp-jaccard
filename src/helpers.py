from math import sqrt, log


def jaccard(X, Y):
    return len(set(X).intersection(set(Y))) / len(set(X).union(set(Y)))


def jaccarddirect(X, Y):
    return len(X.intersection(Y)) / len(X.union(Y))


def estimate_jaccard_minhash(L1, L2):
    K = len(L1)
    return len([i for i in range(K) if L1[i] == L2[i]]) / K


def estimate_jaccard_onebitminhash(L1, L2):
    K = len(L1)
    coll = len([i for i in range(K) if L1[i] == L2[i]])
    return 2 * coll / K - 1


def estimate_bucket_prob(L1, L2, p, b):
    K = len(L1)
    coll = len([i for i in range(K) if L1[i] == L2[i]])
    pp = coll / K
    nom = (b - 1) * (b * pp - 1)
    denom = (b * p - 1)**2
    if denom == 0:
        return 0
    if nom / denom > 1:
        return 1
    if nom / denom < 0:
        return 0
    return nom / denom


def estimate_noisy_bucket_minhash(L1, L2, b, scale):
    K = len(L1)
    dist = sum([(L1[i] - L2[i])**2 for i in range(K)])

    nom = 24 * K * scale**2 + b**2 * K - K - 6 * dist
    denom = K * (b + 1) * (b - 1)
    est = nom / denom
    if est < 0:
        return 0
    if est > 1:
        return 1

    return est


def estimate_noisy_minhash(L1, L2, scale):
    K = len(L1)
    dist = sum([(L1[i] - L2[i])**2 for i in range(K)])

    est = 1 - 2 / K * dist + 8 * scale**2
    if est < 0:
        return 0
    if est > 1:
        return 1

    return est


def estimate_randomized_response_minhash(L1, L2, scale):
    K = len(L1)
    coll = len([i for i in range(K) if L1[i] == L2[i]])

    nom = 2 * coll / K - 1
    denom = (2 * scale - 1)**2

    if nom / denom < 0:
        return 0
    if nom / denom > 1:
        return 1
    return nom / denom


def eps_minhash_conversion(eps, tau, k, delta):
    return k / tau + sqrt(k / tau * 3 * log(1/delta))


def eps_minhash_noisy_bucket_conversion(eps, tau, k, delta, b):
    return k / tau * (b - 1) * (1 - 1/b) + \
        (b - 1) * sqrt(3 * log(1/delta) * k / tau * (1-1/b))


def eps_minhash_bucket_conversion(eps, tau, k, delta, b):
    return k / tau * (1 - 1/b) + sqrt(k / tau * (1-1/b) * 3 * log(1/delta))


def eps_onebit_conversion(eps, tau, k, delta):
    return k / (2 * tau) + sqrt(k / (2 * tau) * 3 * log(1/delta))
