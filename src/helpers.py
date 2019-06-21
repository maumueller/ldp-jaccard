def jaccard(X, Y):
    return len(set(X).intersection(set(Y))) / len(set(X).union(set(Y)))

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
    nom = 1 + (b - 1) * b * ( pp * (b - 2) - 1) - 6 * p + 4 * b * p + (3 - 2 * b) * p**2
    denom = (b - 1) * (-1 + p * (6 - 3 * p + b * (-2 + (b - 1) * p)))
    if denom == 0:
        return 0
    return nom / denom

def estimate_noisy_minhash(L1, L2, scale):
    K = len(L1)
    dist = sum([(L1[i] - L2[i])**2 for i in range(K)])

    return 1 - 2 / K * dist + 8 * scale**2 #2 * (1 - (dist - 2 * K * 2 * scale**2) / K) - 1


