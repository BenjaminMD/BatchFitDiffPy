import json


def read_config(config_path):
    with open(config_path) as f:
        dat = json.load(f)
    return dat
