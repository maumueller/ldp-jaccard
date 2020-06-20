def generate_items(n):
    return list(range(n))


def produce_pair(a, threshold=0.8):
    n = len(a)
    t = n - int(n * (1 - threshold) / (1 + threshold))
    return a[:t] + list(range(n + 1, 2 * n + 1 - t))
