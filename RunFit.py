from multiprocessing import Process, Queue
from rsc.recipe import CreateRecipe
from rsc.util import read_config
import rsc.diffpyhelper as dh
import numpy as np
from glob import glob

from datetime import datetime
startTime = datetime.now()


DAT_DIR = './dat/'
OUT_DIR = './res_single/'
CONF_PATH = './FitConfig.json'

print('test')

conf = read_config(CONF_PATH)


def RunFit(dat_file):
    name = dat_file.split('/')[-1].split('.')[0]
    Fit.update_data(dat_file)
    dh.optimize_params_manually(
        Fit.recipe,
        Fit.param_order,
        rmin=Fit.conf.rmin,
        rmax=Fit.conf.rmax,
        rstep=Fit.conf.rstep,
        ftol=1e-5,
        print_step=True
    )
    dh.save_results(Fit.recipe, OUT_DIR, name, Fit.phases)


Fit = CreateRecipe(
        conf,
        ['Ni', 'Fe_bcc', 'Fe2O3'],
        ['sphericalCF', 'sphericalCF', 'sphericalCF']
    )

data_files = glob(f'{DAT_DIR}*.gr')

Fit.update_recipe()
Fit.create_param_order()
Fit.pg.parallel(32)
RunFit(data_files[0])
print(datetime.now() - startTime)

Fit.pg.parallel(1)
Fit.pg._calc.evaluatortype = 'OPTIMIZED'


if __name__ == "__main__":
    queue = Queue()

    for chunk in np.array_split(data_files[1:], len(data_files[1:])//64):
        processes = [Process(target=RunFit(df), args=(df,)) for df in chunk]
        for p in processes:
            p.start()
        for p in processes:
            p.join()

    print(datetime.now() - startTime)
