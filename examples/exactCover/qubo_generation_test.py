import timeit

import gc
import pandas as pd

import examples.exactCover.path_util as pu

serial_code = "gq.generate_qubo_single_threaded(ec)"

numpy_code = '''gq.generate_qubo_numpy_single_threaded(ec)'''

multiprocessing_code = '''gq.generate_qubo_multi_processing(ec, processes=4)'''

multiprocessing_numpy_code = '''gq.generate_qubo_numpy_multi_processing(ec, processes=4)'''


def create_csv(path, ec_size, num_reps=1):
    setup = "import examples.exactCover.generate_qubo as gq \n" \
            "import examples.exactCover.exact_cover_util as ec \n" \
            "ec = ec.generate_exact_cover(" + str(ec_size) + ")"

    serial = timeit.timeit(serial_code, setup=setup, number=num_reps)

    serial_numpy = timeit.timeit(numpy_code, setup=setup, number=num_reps)

    multiprocessing = timeit.timeit(multiprocessing_code, setup=setup, number=num_reps)

    multiprocessing_numpy = timeit.timeit(multiprocessing_numpy_code, setup=setup, number=num_reps)

    data = [['serial', serial], ['serial_numpy', serial_numpy], ['multiprocessing', multiprocessing],
            ['multiprocessing_numpy', multiprocessing_numpy]]

    df = pd.DataFrame(data, columns=['name', 'time'])
    df.set_index('name', inplace=True)
    df['lBits'] = ec_size

    df.to_csv(path, encoding="utf-8")


if __name__ == '__main__':
    folder = pu.qubo_generation_path()
    i = 50
    end = 2500
    step = 50

    while i <= end:
        create_csv(path=folder + '/' + "{:06d}".format(i) + '.csv', ec_size=i, num_reps=1)
        i += step
        if i % 4 == 0:
            gc.collect()
