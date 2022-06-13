from multiprocessing import Process, Queue

from rsc.diffpyfit import DiffpyFit
from rsc.util import read_config
import numpy as np
from glob import glob

from datetime import datetime
startTime = datetime.now()

DAT_DIR = './dat/'
OUT_DIR = './res/'
CONF_PATH = './FitConfig.json'


def multi_run(file):
    Fit.run_simple_fit(file, OUT_DIR)


if __name__ == "__main__":
    conf = read_config(CONF_PATH)
    Fit = DiffpyFit(conf, ['Ni', 'NiO'], ['sphericalCF', 'sphericalCF'])
    data_files = glob(f'{DAT_DIR}*.gr')
    queue = Queue()

    for chunk in np.array_split(data_files, len(data_files)//64):
        processes = [Process(target=multi_run, args=(df,)) for df in chunk]

        for p in processes:
            p.start()

        for p in processes:
            p.join()

    print(datetime.now() - startTime)
