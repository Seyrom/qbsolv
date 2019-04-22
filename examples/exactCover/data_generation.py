import random
import cProfile, pstats, io
import pandas as pd
import examples.exactCover.generate_qubo as gen

from python.dwave_qbsolv.dimod_wrapper import QBSolv
from dwave.system.samplers import DWaveSampler



def profile_method(fnc, *args, save_directory, filename):
    """Profiles any given function and saves it as a .csv and .prof"""
    pr = cProfile.Profile()

    pr.enable()
    fnc(*args)
    pr.disable()

    s = io.StringIO()
    stats = pstats.Stats(pr, stream=s)
    stats.strip_dirs()
    save_path = save_directory + filename

    regex = '.*(generate_qubo)|(\(sample)|(from_qubo)|(solve_exact_cover)|(dwave_qbsolv.qbsolv_binding.run_qbsolv).*'

    stats.print_stats(regex)
    #stats.print_stats()
    print(s.getvalue())
    stats.dump_stats(save_directory + '/prof/' + filename + ".prof")
    with open(save_path + ".csv", 'w+') as f:
        result = s.getvalue()
        result ='ncalls'+result.split('ncalls')[-1]
        result ='\n'.join([','.join(line.rstrip().split(None,6)) for line in result.split('\n')])
        f.write(result)
        f.close()


def add_logical_bits_column_to_csv(path_of_file, lBits):
    """Adds a new logicalBits column containing how many logical bits were used for this exactCover"""
    df = pd.read_csv(path_of_file)
    new_column = pd.DataFrame({'logicalBits': [lBits, lBits, lBits, lBits, lBits, lBits]})
    df = df.merge(new_column, left_index = True, right_index = True)
    df.to_csv(path_of_file)


def generate_exact_cover(num_of_subsets):
    """Generates a new exact cover problem with the given number of random filled subsets"""
    subset = set()
    while len(subset) < num_of_subsets:
        subset.add(frozenset(random.sample(range(num_of_subsets), random.randint(1, num_of_subsets - 1))))
    return list(subset)

def solve_exact_cover(exact_cover):
    """Generates a QUBO and then samples it with qbsolv to solve the given exact cover problem"""
    #QUBO = generate_qubo_single_threaded(exact_cover)
    #QBSolv().sample_qubo(QUBO, verbosity =-1)

def solve_exact_cover_multi_threaded(exact_cover):
    """Generates a QUBO and then samples it with qbsolv to solve the given exact cover problem"""
    QUBO = gen.generate_qubo_numpy_multi_processing(exact_cover, nProcs= 4)
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
    dir = '/home/patrickb/GitRepos/qbsolv/examples/exactCover/qbsolvScalingData/'
    for variable_count in [x for x in range(start, end) if x % step  == 0]:
        for iter in range(0, iterations):
            print('Solving QUBO of size ' + str(variable_count) + ' iteration: ' + "{:05d}".format(iter))
            ec = generate_exact_cover(variable_count)
            filename = 'exactCover_rep_' + str(iter) + '__' + str(variable_count)
            profile_method(solve_exact_cover, ec, save_directory = dir, filename = filename)
            add_logical_bits_column_to_csv(dir + filename + '.csv', variable_count)



#create_test_data(start = 100, end = 2000, step = 50, iterations= 1)

ec = generate_exact_cover(200)
#profile_method(solve_exact_cover, ec, save_directory = "/home/patrickb/GitRepos/qbsolv/examples/exactCover/qbsolvScalingData/", filename = "test")

solve_exact_cover_multi_threaded(ec)
