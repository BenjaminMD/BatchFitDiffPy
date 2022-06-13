from rsc.diffpyfit import DiffpyFit
from rsc.util import read_config
from glob import glob


DAT_DIR = './dat/'
OUT_DIR = './res/'
CONF_PATH = './FitConfig.json'

if __name__ == '__main__':
    conf = read_config(CONF_PATH)
    Fit = DiffpyFit(conf, ['NiO'], ['sheetCF'])
    for data_file in glob(f'{DAT_DIR}/*.gr'):
        Fit.run_simple_fit(data_file, OUT_DIR)
