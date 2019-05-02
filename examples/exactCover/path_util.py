import os


def path():
    return os.path.dirname(os.path.abspath(__file__))


def data_path():
    data_ = path() + '/data'
    os.makedirs(data_, exist_ok=True)
    return data_


def qubo_generation_path():
    gen_ = data_path() + '/qubo_gen'
    os.makedirs(gen_, exist_ok=True)
    return gen_


def scale_path():
    scale_ = data_path() + '/scale'
    os.makedirs(scale_, exist_ok=True)
    return scale_


def scale_iter_path(iteration):
    iter_ = scale_path() + '/iter_' + "{:03d}".format(iteration)
    os.makedirs(iter_, exist_ok=True)
    return iter_


def scale_prof_path(iteration):
    prof_ = scale_iter_path(iteration) + '/prof'
    os.makedirs(prof_, exist_ok=True)
    return prof_


if __name__ == '__main__':
    qubo_generation_path()
    scale_path()
