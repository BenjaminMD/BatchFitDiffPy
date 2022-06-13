from diffpy.srfit.fitbase import FitResults
from recipe import CreateRecipe
import diffpyhelper as dh


class DiffpyFit(CreateRecipe):
    def __init__(self, conf, phases, char_function):
        super().__init__(conf, phases, char_function)

    def run_simple_fit(self, data_file):
        if not self.recipe:
            self.update_data(data_file)
            self.update_recipe()
            self.default_restraints()
            self.create_param_order()

        else:
            self.update_data(data_file)

        dh.optimize_params_manually(
            self.recipe,
            self.param_order,
            rmin=self.conf.rmin,
            rmax=self.conf.rmax,
            rstep=self.conf.rstep,
            ftol=1e-5,
            print_step=False
        )

        self.name = data_file.split('/')[-1].split('.')[0]

        res = FitResults(self.recipe)
        res.saveResults(f'{self.out}{self.name}.res')

    def run_molarcontribution_fit():
        pass
