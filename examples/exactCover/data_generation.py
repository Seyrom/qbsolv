import examples.exactCover.generate_qubo as gq
import examples.exactCover.exactcover_util as ecg
from examples.exactCover.util import profile_method, post_processing_csv

from python.dwave_qbsolv.dimod_wrapper import QBSolv


def solve_exact_cover(exact_cover):
    """Generates a QUBO and then samples it with qbsolv to solve the given exact cover problem"""
    QUBO = gq.generate_qubo_single_threaded(exact_cover)
    QBSolv().sample_qubo(QUBO, verbosity =-1)

def  solve_exact_cover_numpy(exact_cover):
    QUBO = gq.generate_qubo_numpy_single_threaded(exact_cover)
    QBSolv().sample_qubo(QUBO, verbosity = -1)

def solve_exact_cover_multi_processing(exact_cover):
    """Generates a QUBO and then samples it with qbsolv to solve the given exact cover problem"""
    QUBO = gq.generate_qubo_numpy_multi_processing(exact_cover, nProcs= 4)
    QBSolv().sample_qubo(QUBO, verbosity =-1)

def solve_exact_cover_multi_processing_numpy(exact_cover):
    QUBO = gq.generate_qubo_numpy_multi_processing(exact_cover, nProcs= 4)
    QBSolv().sample_qubo(QUBO, verbosity =-1)

#def solve_exact_cover_dwave(exact_cover):
    #solver_limit = 50
    #solver = 'DW_2000Q_2_1'
    #token = "LMUM-e785642c5cb38b5a63c33da26f4fa8b185359412"
    #endpoint = 'https://cloud.dwavesys.com/sapi'
    #sampler = DWaveSampler(solver_limit = solver_limit, solver = solver, token = token, endpoint = endpoint)
    #QUBO = generate_qubo_single_threaded(exact_cover)
    #QBSolv().sample_qubo(QUBO, verbosity = -1)

def create_test_data(start, end, step, iterations):
    dir = '/home/patrickb/GitRepos/qbsolv/examples/exactCover/qbsolvScalingData/multi_processing_numpy/'
    for variable_count in [x for x in range(start, end) if x % step  == 0]:
        for iter in range(0, iterations):
            print('Solving QUBO of size ' + str(variable_count) + ' iteration: ' + "{:05d}".format(iter))
            ec = ecg.generate_exact_cover(variable_count)
            filename = 'exactCover_rep_' + "{:02d}".format(iter) + '_' + "{:06d}".format(variable_count)
            profile_method(solve_exact_cover_numpy, ec, save_directory = dir, filename = filename)
            post_processing_csv(dir + filename + '.csv', lBits=variable_count)

if __name__ == '__main__':
    create_test_data(start = 500, end = 550, step = 50, iterations= 1)


