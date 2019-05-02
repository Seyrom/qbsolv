from functools import partial
from multiprocessing import Pool

import numpy as np

from .exact_cover_util import generate_exact_cover


def generate_qubo_single_threaded(exact_cover, b=1):
    """Generates an upper triangular QUBO matrix for the given exact cover"""
    a = len(exact_cover) * b + 1
    q = dict()
    for j, cur_subset in enumerate(exact_cover):
        q[(j, j)] = -len(cur_subset)
        for i, oth_subset in [(i, oth_subset) for i, oth_subset in enumerate(exact_cover) if j < i]:
            # upper triangular matrix
            q[(j, i)] = 4 * a * len(cur_subset & oth_subset)
    return q


def generate_qubo_numpy_single_threaded(exact_cover, b=1):
    """Generates an upper triangular QUBO matrix as a numpy array for the given exact cover"""
    a = len(exact_cover) * b + 1
    dim = len(exact_cover)
    arr = np.empty(shape=(dim, dim), dtype=np.dtype('>i4'))
    for j, cur_subset in enumerate(exact_cover):
        arr[j] = [4 * a * len(cur_subset & oth_subset) if j < i else -len(cur_subset) if i == j else 0 for i, oth_subset
                  in enumerate(exact_cover)]
    return to_dict(arr)


def fill_col(i, ec, a):
    col = ec[i]
    dic_temp = dict()
    dic_temp[(i, i)] = -len(col)
    for j, subset in [(j, subset) for j, subset in enumerate(ec) if j < i]:
        # upper triangular matrix
        dic_temp[(j, i)] = 4 * a * len(col & subset)
    return dic_temp


def generate_qubo_multi_processing(exact_cover, processes, b=1):
    """Generates an upper triangular QUBO matrix for the given exact cover with multi processing"""

    a = len(exact_cover) * b + 1
    q = dict()

    prod = partial(fill_col, ec=exact_cover, a=a)
    pool = Pool(processes=processes)
    result = pool.map(prod, range(len(exact_cover)))
    pool.close()
    pool.join()
    for d in result:
        q.update(d)
    return q


def fill_col_numpy(i, ec, a):
    col = ec[i]

    arr = np.array(
        [4 * a * len(col & oth_subset) if j > i else -len(col) if i == j else 0 for j, oth_subset in enumerate(ec)])
    return arr, i


def generate_qubo_numpy_multi_processing(exact_cover, processes, b=1):
    """Generates an upper triangular QUBO matrix with numpy for the given exact cover with multi processing"""

    a = len(exact_cover) * b + 1
    dim = len(exact_cover)
    arr = np.empty(shape=(dim, dim), dtype=np.dtype('>i4'))

    prod = partial(fill_col_numpy, ec=exact_cover, a=a)
    pool = Pool(processes=processes)
    result = pool.map(prod, range(len(exact_cover)))
    pool.close()
    pool.join()
    for row, i in result:
        arr[i] = row

    return to_dict(arr)


def to_dict(arr):
    q = dict()

    for i, ar in enumerate(arr):
        for j, val in [(j, val) for j, val in enumerate(ar) if i == j or i < j]:
            q[(i, j)] = val
    return q


if __name__ == '__main__':
    ec = generate_exact_cover(100)
    Q1 = generate_qubo_single_threaded(ec)
    Q2 = generate_qubo_numpy_single_threaded(ec)
    Q3 = generate_qubo_multi_processing(ec, 4)
    Q4 = generate_qubo_numpy_multi_processing(ec, 4)

    print(Q1 == Q2)
    print(Q2 == Q3)
    print(Q3 == Q4)
