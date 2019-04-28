import random


def generate_exact_cover(num_of_subsets):
    """Generates a new exact cover problem with the given number of random filled subsets"""
    subset = set()
    while len(subset) < num_of_subsets:
        subset.add(frozenset(random.sample(range(num_of_subsets), random.randint(1, num_of_subsets - 1))))
    return list(subset)