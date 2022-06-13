from multiprocessing import Process, Queue

from rsc.diffpyfit import DiffpyFit
from rsc.util import read_config
from glob import glob


DAT_DIR = './dat/'
OUT_DIR = './res/'
CONF_PATH = './FitConfig.json'


def multi_run(file):
    Fit.run_simple_fit(file, OUT_DIR)



if __name__ == "__main__":
    conf = read_config(CONF_PATH)
    Fit = DiffpyFit(conf, ['Ni'], ['sphericalCF'])
    gr_files = glob(DAT_DIR + '*.gr')
    queue = Queue()

    processes = [Process(target=multi_run, args=(x,)) for x in gr_files]

    for p in processes:
        p.start()

    for p in processes:
        p.join()