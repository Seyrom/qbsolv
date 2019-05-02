import gc

import examples.exactCover.exact_cover_util as ecg
import examples.exactCover.generate_qubo as gq
import examples.exactCover.io_util as io
import examples.exactCover.path_util as pu
from python.dwave_qbsolv.dimod_wrapper import QBSolv


def solve_exact_cover(exact_cover):
    qubo = gq.generate_qubo_numpy_multi_processing(exact_cover, processes=4)
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
            ec = ecg.generate_exact_cover(variable_count)
            subfolder = pu.scale_iter_path(i)
            filename = '/' + "{:06d}".format(variable_count)
            io.profile_method(solve_exact_cover, ec, save_directory=subfolder, filename=filename, iteration=i)
            io.post_processing_csv(subfolder + filename + '.csv', lbits=variable_count)
            if i % 4 == 0:
                gc.collect()


if __name__ == '__main__':
    create_test_data(start=50, end=4000, step=25, iterations=75)
