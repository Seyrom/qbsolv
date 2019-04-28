import examples.exactCover.generate_qubo as gq
import pandas as pd
import numpy as np
import timeit
import examples.exactCover.exactcover_util as ec



serial_code = "gq.generate_qubo_single_threaded(ec)"

numpy_code = '''gq.generate_qubo_numpy_single_threaded(ec)'''

multiprocessing_code = '''gq.generate_qubo_multi_processing(ec, nProcs= 4)'''

multiprocessing_numpy_code = '''gq.generate_qubo_numpy_multi_processing(ec, nProcs = 4)'''


def create_csv(path, ec_size, num_reps = 1):

    setup = "import examples.exactCover.generate_qubo as gq \n" \
            "import examples.exactCover.exactcover_util as ec \n" \
            "ec = ec.generate_exact_cover("+str(ec_size)+")"

    serial = timeit.timeit(serial_code, setup=setup, number=num_reps)

    serial_numpy = timeit.timeit(numpy_code, setup=setup, number=num_reps)

    multiprocessing = timeit.timeit(multiprocessing_code, setup=setup, number=num_reps)

    multiprocessing_numpy = timeit.timeit(multiprocessing_numpy_code, setup=setup, number=num_reps)

    data ={ "serial" : serial,
            "serial_numpy" : serial_numpy,
            "multiprocessing" : multiprocessing,
            "multiprocessing_numpy" : multiprocessing_numpy
            }
    df = pd.Series(data).to_frame('time')

    df.to_csv(path)


if __name__ == '__main__':
    folder = '/home/patrickb/GitRepos/qbsolv/examples/exactCover/qbsolvScalingData/qubo_generation/'
    start = 50
    end = 2000
    step = 50
    cur = start

    while cur <= end:
        file = 'qubo_generation_' + "{:06d}".format(cur) + '.csv'
        cur += step
        path = folder + file
        create_csv(path=path, ec_size=50, num_reps=30)