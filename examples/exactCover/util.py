import cProfile
import io
import pstats
import re
import os
import examples.exactCover.path_util as pu

import pandas as pd


def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        pr = cProfile.Profile()
        try:
            pr.enable()
            result = func(*args, **kwargs)
            pr.disable()
            s = io.StringIO()
            stats = pstats.Stats(pr, stream=s)
            stats.strip_dirs()
            stats.sort_stats('cumulative')
            return result
        finally:
            regex = str(func)
            stats.print_stats(regex)
            print(s.getvalue())

    return profiled_func


def profile_method(fnc, *args, save_directory, filename, iteration):
    """Profiles any given function and saves it as a .csv and .prof"""
    pr = cProfile.Profile()

    pr.enable()
    fnc(*args)
    pr.disable()

    s = io.StringIO()
    stats = pstats.Stats(pr, stream=s)
    stats.strip_dirs()

    prof_path = pu.scale_prof_path(iteration)
    stats.dump_stats(prof_path + '/' + filename + ".prof")


    regex = '.*(solve_exact_cover\S*)|.*(\(generate_qubo\S*)|.*(sample_qubo)|.*(\(sample)' \
            '|(dwave_qbsolv.qbsolv_binding.run_qbsolv)|.*(from_qubo)|.*(to_qubo)'

    stats.print_stats(regex)


    with open(save_directory + filename + ".csv", 'w+') as f:
        result = s.getvalue()
        result ='ncalls'+result.split('ncalls')[-1]
        result ='\n'.join([','.join(line.rstrip().split(None,6)) for line in result.split('\n')])
        f.write(result)
        f.close()



def post_processing_csv(path_of_file, lBits):
    """Adds a new logicalBits column containing how many logical bits were used
    for this exactCover and deletes unused columns"""
    df = pd.read_csv(path_of_file)
    df.drop(['ncalls', 'tottime', 'percall', 'percall.1'], inplace=True, axis=1)
    df.rename(columns={'filename:lineno(function)':'function'}, inplace=True)
    df.insert(1, 'logical Bits', lBits)
    # removing Classname.py:linenumber and paranthesis
    regex = '(\S*.py:\d+)|\(|\)|{|}'
    df['function'] = df['function'].apply(lambda x : re.sub(regex,'', x))
    df['cumtime'] = df['cumtime'].round(5)
    df.to_csv(path_of_file)