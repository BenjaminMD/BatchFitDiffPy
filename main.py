from rsc.fitconfig import RecipeClass, read_config
import json


DAT_PATH = './dat'
OUT_PATH = './res'
CONF_PATH = './rsc/FitConfig.json'

if __name__ == '__main__':
    conf = read_config(CONF_PATH)
    Fit = RecipeClass(conf, dat, ['NiO'], ['sheetCF'])
