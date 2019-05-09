import glob
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from path_util import scale_path

# CSV Structure
'''
function                                    ,cumtime        ,lBits
to_qubo                                     ,0.484          ,950
from_qubo                                   ,2.328          ,950
sample                                      ,5.567          ,950
sample_qubo                                 ,7.916          ,950
dwave_qbsolv.qbsolv_binding.run_qbsolv      ,5.075          ,950
generate_qubo_numpy_multi_processing        ,4.71           ,950
solve_exact_cover                           ,12.627         ,950


'''


def over_all_plot():
    path = scale_path()
    subfolders = [f.path for f in os.scandir(path) if f.is_dir()]
    lbits = []
    total_runtime = []
    qubo_generation = []
    qubo_sampling = []

    for subfolder in subfolders:
        files = sorted([f for f in glob.glob(subfolder + '/' + "*.csv", recursive=True)])
        temp_total_runtime = []
        temp_qubo_generation = []
        temp_qubo_sampling = []
        temp_lbits = []

        for file in files:
            df = pd.read_csv(file, delimiter=',', encoding="utf-8")
            df.set_index('function', inplace=True)
            temp_total_runtime.append(df.loc['solve_exact_cover', 'cumtime'])
            temp_qubo_generation.append(df.loc['generate_qubo_numpy_multi_processing', 'cumtime'])
            temp_qubo_sampling.append(df.loc['sample_qubo', 'cumtime'])
            temp_lbits.append(df.loc['solve_exact_cover', 'lBits'])

        total_runtime.append(temp_total_runtime)
        qubo_generation.append(temp_qubo_generation)
        qubo_sampling.append(temp_qubo_sampling)
        lbits.append(temp_lbits)

    np_qbits = np.array(lbits)
    np_total_runtime = np.array(total_runtime)
    np_qubo_generation = np.array(qubo_generation)
    np_qubo_sampling = np.array(qubo_sampling)

    lbits = np.mean(np_qbits, axis=0)
    total_runtime = np.mean(np_total_runtime, axis=0)
    qubo_generation = np.mean(np_qubo_generation, axis=0)
    qubo_sampling = np.mean(np_qubo_sampling, axis=0)

    plt.plot(lbits, total_runtime, label='total_runtime')
    plt.plot(lbits, qubo_generation, label='QUBO_generation')
    plt.plot(lbits, qubo_sampling, label='QUBO_sampling')
    plt.title('Total time for solving a QUBO')
    plt.xlabel('# logical Bits')
    plt.ylabel('time in s')
    plt.legend(loc='upper left')
    plt.show()


def qubo_sampling_plot():
    path = scale_path()
    subfolders = [f.path for f in os.scandir(path) if f.is_dir()]
    lbits = []
    sampling_overall = []
    bqm_transformation = []
    bqm_sampling = []

    for subfolder in subfolders:
        files = sorted([f for f in glob.glob(subfolder + '/' + "*.csv", recursive=True)])
        temp_sampling_overall = []
        temp_bqm_transformation = []
        temp_bqm_sampling = []
        temp_lbits = []

        for file in files:
            df = pd.read_csv(file, delimiter=',', encoding="utf-8")
            df.set_index('function', inplace=True)
            temp_sampling_overall.append(df.loc['sample_qubo', 'cumtime'])
            temp_bqm_transformation.append(df.loc['from_qubo', 'cumtime'])
            temp_bqm_sampling.append(df.loc['sample', 'cumtime'])
            temp_lbits.append(df.loc['sample_qubo', 'lBits'])

        sampling_overall.append(temp_sampling_overall)
        bqm_transformation.append(temp_bqm_transformation)
        bqm_sampling.append(temp_bqm_sampling)
        lbits.append(temp_lbits)

    np_qbits = np.array(lbits)
    np_total_runtime = np.array(sampling_overall)
    np_qubo_generation = np.array(bqm_transformation)
    np_qubo_sampling = np.array(bqm_sampling)

    lbits = np.mean(np_qbits, axis=0)
    sampling_overall = np.mean(np_total_runtime, axis=0)
    bqm_transformation = np.mean(np_qubo_generation, axis=0)
    bqm_sampling = np.mean(np_qubo_sampling, axis=0)

    plt.plot(lbits, sampling_overall, label='QUBO_sampling')
    plt.plot(lbits, bqm_transformation, label='to_bqm')
    plt.plot(lbits, bqm_sampling, label='sample')
    plt.title('Total time for sampling a QUBO')
    plt.xlabel('# logical Bits')
    plt.ylabel('time in s')
    plt.legend(loc='upper left')
    plt.show()


if __name__ == '__main__':
    over_all_plot()
    qubo_sampling_plot()

