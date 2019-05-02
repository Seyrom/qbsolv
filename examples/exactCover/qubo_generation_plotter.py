import glob

import matplotlib.pyplot as plt
import pandas as pd

from path_util import qubo_generation_path


# CSV Structure
'''
                        ,time                   ,lBits
serial                  ,0.0016476050004712306  ,50
serial_numpy            ,0.002307472997927107   ,50
multiprocessing         ,0.014695772002596641   ,50
multiprocessing_numpy   ,0.014273968001361936   ,50
'''


def get_data(path):
    """"Gives back a list of all .csv files in the given path"""
    files = [f for f in glob.glob(path + "/*.csv", recursive=True)]
    return files


def plot():
    """Creates a plot of the total runtime of a given method"""
    path = qubo_generation_path()
    files = sorted(get_data(path))

    lbits = []
    serial = []
    serial_numpy = []
    multi = []
    multi_numpy = []

    for file in files:
        df = pd.read_csv(file, delimiter=',', encoding="utf-8")
        df.set_index('name', inplace=True)
        lbits.append(df['lBits'][0])
        serial.append(df.loc['serial', 'time'])
        serial_numpy.append(df.loc['serial_numpy', 'time'])
        multi.append(df.loc['multiprocessing', 'time'])
        multi_numpy.append(df.loc['multiprocessing_numpy', 'time'])

    plt.plot(lbits, serial, label='serial')
    plt.plot(lbits, serial_numpy, label='serial_numpy')
    plt.plot(lbits, multi, label='multi_processing')
    plt.plot(lbits, multi_numpy, label='multi_processing_numpy')
    plt.title('Total time for QUBO Generation')
    plt.xlabel('# logical Bits')
    plt.ylabel('time in s')
    plt.legend(loc='upper left')
    plt.show()


if __name__ == '__main__':
    plot()
