import gc

from exact_cover_util import generate_exact_cover
from io_util import profile_method, post_processing_csv
from path_util import scale_iter_path
from python.dwave_qbsolv.dimod_wrapper import QBSolv
from generate_qubo import generate_qubo_numpy_multi_processing


def solve_exact_cover(exact_cover):
    qubo = generate_qubo_numpy_multi_processing(exact_cover, processes=4)
    QBSolv().sample_qubo(qubo, verbosity=-1)


# def solve_exact_cover_dwave(exact_cover):
# solver_limit = 50
# solver = 'DW_2000Q_2_1'
# token = "LMUM-e785642c5cb38b5a63c33da26f4fa8b185359412"
# endpoint = 'https://cloud.dwavesys.com/sapi'
# sampler = DWaveSampler(solver_limit = solver_limit, solver = solver, token = token, endpoint = endpoint)
# QUBO = generate_qubo_single_threaded(exact_cover)
# QBSolv().sample_qubo(QUBO, verbosity = -1)

def create_test_data(start, end, step, iterations):
    for variable_count in [x for x in range(start, end) if x % step == 0]:
        for i in range(0, iterations):
            ec = generate_exact_cover(variable_count)
            subfolder = scale_iter_path(i)
            filename = '/' + "{:06d}".format(variable_count)
            print("Currently solving exact cover of size: " + str(variable_count) + "iteration: #" + str(i))
            profile_method(solve_exact_cover, ec, save_directory=subfolder, filename=filename, iteration=i)
            print("Finished solving exact cover of size: " + str(variable_count) + "iteration: #" + str(i))
            post_processing_csv(subfolder + filename + '.csv', lbits=variable_count)
            if i % 4 == 0:
                gc.collect()


if __name__ == '__main__':
    create_test_data(start=50, end=4000, step=25, iterations=50)
