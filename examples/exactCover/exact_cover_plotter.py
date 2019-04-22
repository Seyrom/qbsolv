import glob
import pandas as pd
import matplotlib.pyplot as plt

#   ,ncalls,    tottime,    percall,    cumtime,    percall.1,  filename:lineno(function),                  logicalBits
#                                                               binary_quadratic_model.py:1887(from_qubo)
#                                                               dimod_wrapper.py:31(sample)
#                                                               sampler.py:159(sample_qubo)
#                                                               data_generation.py:52(generate_qubo)
#                                                               {dwave_qbsolv.qbsolv_binding.run_qbsolv}
#                                                               data_generation.py:64(solve_exact_cover)


def get_data(path):
    """"Gives back a list of all .csv files in the given path"""
    files = [f for f in glob.glob(path + "*.csv", recursive=True)]
    return files

def plot(filename):
    """Creates a plot of the total runtime of a given method"""
    path = '/home/patrickb/GitRepos/qbsolv/examples/exactCover/qbsolvScalingData/'
    files = sorted(get_data(path))
    lBits = []
    time = []

    for file in files:
        df = pd.read_csv(file)
        lBits.append(df['logicalBits'][0])
        for i, t in enumerate(df['cumtime']):
            if(df['filename:lineno(function)'][i] == filename ):
               time.append(t)

    plt.plot(lBits, time, 'ro')
    plt.title('Total runtime of method call: ' + filename)
    plt.xlabel('# logical Bits')
    plt.ylabel('time in s')
    plt.show()


plot('data_generation.py:64(solve_exact_cover)')

# solve_exact_cover calls:
# generate_qubo and sample_qubo
# sample_qubo calls:
# from_qubo and sample
# sample calls binding.run_qbsolv