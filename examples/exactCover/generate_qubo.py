import cProfile
import io
import pstats
import random

import numpy as np
from multiprocessing import Pool
from functools import partial


def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        pr = cProfile.Profile()
        try:
            pr.enable()
            result = func(*args, **kwargs)
            pr.disable()
            s = io.StringIO()
            stats = pstats.Stats(pr, stream=s)
            stats.strip_dirs()
            stats.sort_stats('cumulative')
            return result
        finally:
            regex = str(func)
            stats.print_stats(regex)
            print(s.getvalue())

    return profiled_func


@do_cprofile
def generate_qubo_single_threaded(exact_cover, b=1):
    """Generates an upper triangular QUBO matrix for the given exact cover"""
    a = len(exact_cover) * b + 1
    Q = dict()
    for j, cur_subset in enumerate(exact_cover):
        Q[(j, j)] = -len(cur_subset)
        for i, oth_subset in [(i, oth_subset) for i, oth_subset in enumerate(exact_cover) if j < i]:
            # upper triangular matrix
            Q[(j, i)] = 4 * a * len(cur_subset & oth_subset)
    return Q

@do_cprofile
def generate_qubo_numpy_single_threaded(exact_cover, b=1):
    """Generates an upper triangular QUBO matrix as a numpy array for the given exact cover"""
    a = len(exact_cover) * b + 1
    dim = len(exact_cover)
    #arr = np.zeros(shape= (dim, dim))
    arr = np.empty(shape= (dim, dim), dtype=np.dtype('>i4'))
    for j, cur_subset in enumerate(exact_cover):
        arr[j] = [4 * a * len(cur_subset & oth_subset) if j < i else -len(cur_subset) if i == j else 0 for i, oth_subset in enumerate(exact_cover)]
    return to_dict(arr)

def fill_col(i, ec, a):
    col = ec[i]
    dic_temp = dict()
    dic_temp[(i, i)] = -len(col)
    for j, subset in [(j, subset) for j, subset in enumerate(ec) if j < i]:
        # upper triangular matrix
        dic_temp[(j, i)] = 4 * a * len(col & subset)
    return dic_temp


@do_cprofile
def generate_qubo_multi_processing(exact_cover, nProcs, b=1):
    """Generates an upper triangular QUBO matrix for the given exact cover with multi processing"""

    a = len(exact_cover) * b + 1
    Q = dict()

    prod = partial(fill_col, ec = exact_cover, a = a)
    pool = Pool(processes=nProcs)
    result = pool.map(prod, range(len(exact_cover)))
    for d in result:
        Q.update(d)

    return Q

def fill_col_numpy(i, ec, a):
    col = ec[i]


    arr = np.array([4 * a * len(col & oth_subset) if j > i else -len(col) if i == j else 0 for j, oth_subset in enumerate(ec)])
    return (arr, i)


@do_cprofile
def generate_qubo_numpy_multi_processing(exact_cover, nProcs, b=1):
    """Generates an upper triangular QUBO matrix with numpy for the given exact cover with multi processing"""

    a = len(exact_cover) * b + 1
    dim = len(exact_cover)
    arr = np.empty(shape= (dim, dim), dtype=np.dtype('>i4'))

    prod = partial(fill_col_numpy, ec = exact_cover, a = a)
    pool = Pool(processes=nProcs)
    result = pool.map(prod, range(len(exact_cover)))
    for row, i in result:
        arr[i] = row

    return to_dict(arr)

def to_dict(arr):
    Q = dict()

    for i,ar in enumerate(arr):
        for j, val in [(j, val) for j, val in enumerate(ar) if i == j or i < j]:
            Q[(i,j)] = val
    return Q;

def generate_exact_cover(num_of_subsets):
    """Generates a new exact cover problem with the given number of random filled subsets"""
    subset = set()
    while len(subset) < num_of_subsets:
        subset.add(frozenset(random.sample(range(num_of_subsets), random.randint(1, num_of_subsets - 1))))
    return list(subset)

ec = generate_exact_cover(800)
Q1 = generate_qubo_single_threaded(ec)
Q2 = generate_qubo_numpy_single_threaded(ec)
Q3 = generate_qubo_multi_processing(ec, 4)
Q4 = generate_qubo_numpy_multi_processing(ec, 4)

print(Q1 == Q2)
print(Q2 == Q3)
print(Q3 == Q4)
