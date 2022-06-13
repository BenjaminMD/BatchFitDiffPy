from dataclasses import dataclass
import json


@dataclass(frozen=True)
class FitConfig():


    qdamp = config['MetaData']['qdamp']
    qbroad = config['MetaData']['qbroad']
    rmin = config['FitData']['rmin']
    rmax = config['FitData']['rmax']
    rstep =config['FitData']['rstep']
