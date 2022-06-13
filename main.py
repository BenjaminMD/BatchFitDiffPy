from rsc.diffpyfit import DiffpyFit
from rsc.util import read_config
from glob import glob


DAT_PATH = './dat'
OUT_PATH = './res'
CONF_PATH = './FitConfig.json'

if __name__ == '__main__':
    conf = read_config(CONF_PATH)
    Fit = DiffpyFit(conf, ['NiO'], ['sheetCF'])
    for data_file in glob(f'{DAT_PATH}/*.gr'):
        Fit.run_simple_fit(data_file)  
