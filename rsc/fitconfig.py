import diffpy.srfit.pdf.characteristicfunctions as CF
from dataclasses import dataclass


@dataclass(frozen=True)
class FitConfig():
    __slots__ = ["qdamp", "qbroad", "rmin", "rmax", "rstep"]
    qdamp: float
    qbroad: float
    rmin: float
    rmax: float
    rstep: float

    def __call__(self):
        return {'qdamp': self.qdamp, 'qbroad': self.qbroad}

    def fetch_function(self, phase, function):
        func_param = {
            'sphericalCF':
                (CF.sphericalCF,
                    ['r', f'{phase}_psize']),
            'spheroidalCF':
                (CF.spheroidalCF,
                    ['r', f'{phase}_erad', f'{phase}_prad']),
            'spheroidalCF2':
                (CF.spheroidalCF2,
                    ['r', '{phase}_psize', f'{phase}_axrat']),
            'lognormalSphericalCF':
                (CF.lognormalSphericalCF,
                    ['r', f'{phase}_psize', f'{phase}_psig']),
            'sheetCF':
                (CF.sheetCF,
                    ['r', f'{phase}_sthick']),
            'shellCF':
                (CF.shellCF,
                    ['r', f'{phase}_radius', f'{phase}_thickness']),
            'shellCF2':
                (CF.shellCF,
                    ['r', f'{phase}_a', f'{phase}_delta']),
            'bulkCF':
                (lambda r: 1,
                    ['r']),
        }
        return func_param[function]


