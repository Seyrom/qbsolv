import timeit

import gc
import pandas as pd

from path_util import qubo_generation_path


serial_code = "generate_qubo_single_threaded(ec)"

numpy_code = '''generate_qubo_numpy_single_threaded(ec)'''

multiprocessing_code = '''generate_qubo_multi_processing(ec, processes=4)'''

multiprocessing_numpy_code = '''generate_qubo_numpy_multi_processing(ec, processes=4)'''


def create_csv(path, ec_size, num_reps=1):
    setup = "from generate_qubo import generate_qubo_single_threaded, generate_qubo_numpy_single_threaded," \
            " generate_qubo_multi_processing, generate_qubo_numpy_multi_processing \n" \
            "from exact_cover_util import generate_exact_cover \n" \
            "ec = generate_exact_cover(" + str(ec_size) + ")"

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
    folder = qubo_generation_path()
    i = 50
    end = 3000
    step = 25

    while i <= end:
        create_csv(path=folder + '/' + "{:06d}".format(i) + '.csv', ec_size=i, num_reps=30)
        i += step
        print("Finishhed Qubo size" + str(i))
        if i % 4 == 0:
            gc.collect()
