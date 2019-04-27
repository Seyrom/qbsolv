import glob
import pandas as pd
import matplotlib.pyplot as plt


# CSV Structure
'''
    ,cumtime    ,logical Bits   ,function
0   ,0.125      ,500            ,to_qubo
1   ,0.584      ,500            ,from_qubo
2   ,2.083      ,500            ,sample
3   ,2.674      ,500            ,sample_qubo
4   ,1.955      ,500            ,dwave_qbsolv.qbsolv_binding.run_qbsolv
5   ,1.308      ,500            ,generate_qubo_numpy_single_threaded
6   ,3.982      ,500            ,solve_exact_cover_numpy

'''




def get_data(path):
    """"Gives back a list of all .csv files in the given path"""
    files = [f for f in glob.glob(path + "*.csv", recursive=True)]
    return files

def plot(filename):
    """Creates a plot of the total runtime of a given method"""
    path = '/home/patrickb/GitRepos/qbsolv/examples/exactCover/qbsolvScalingData/single_threaded'
    files = sorted(get_data(path))
    lBits = []
    time = []

    for file in files:
        df = pd.read_csv(file)
        lBits.append(df['logicalBits'][0])
        for i, t in enumerate(df['cumtime']):
            if(df['filename:lineno(function)'][i] == filename ):
               time.append(t)

    plt.plot(lBits, time)
    plt.title('Total runtime of method call: ' + filename)
    plt.xlabel('# logical Bits')
    plt.ylabel('time in s')
    plt.show()


if __name__ == '__main__':
    plot('data_generation.py:64(solve_exact_cover)')

# solve_exact_cover calls:
# generate_qubo and sample_qubo
# sample_qubo calls:
# from_qubo and sample
# sample calls binding.run_qbsolv