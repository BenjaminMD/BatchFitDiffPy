from diffpy.srfit.fitbase import FitResults
from rsc.recipe import CreateRecipe
import rsc.diffpyhelper as dh


class DiffpyFit(CreateRecipe):
    def __init__(self, conf, phases, char_function):
        super().__init__(conf, phases, char_function)

    def run_simple_fit(self, data_file, out_dir):
        if not hasattr(self, 'recipe'):
            self.update_data(data_file)
            self.update_recipe()
            self.default_restraints()
            self.create_param_order()

        else:
            self.update_data(data_file)
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

    def save_results(self, out_dir, name_ext=''):
        res = FitResults(self.recipe)
        #print(name_ext)
        res.saveResults(f'{out_dir}{self.name}{name_ext}.res')


    def run_molarcontribution_fit(self, data_file, out_dir, molar_limit):
        self.run_simple_fit(data_file, out_dir)
        self.removed_phase = []
        for phase in self.phases:
            scale = self.get_mol_contribution(phase)
            #print(f'{phase} scale: {scale}')
            if scale < molar_limit:
                self.remove_phase(phase)
                self.removed_phase.append(phase)
                self.update_recipe()
                #self.recipe.show()
                self.create_param_order()
                #print(self.equation, self.phases, self.param_order, self.functions)
                self.run_simple_fit(data_file, out_dir)
        if self.removed_phase:
            res = FitResults(self.recipe)
            self.update_recipe()
            
            res.saveResults(f'{out_dir}{self.name}{self.removed_phase}.res')
            [self.add_phase(phase) for phase in self.removed_phase]
            self.update_recipe()
            self.run_simple_fit(data_file, out_dir)
        else:
            res = FitResults(self.recipe)
            self.update_recipe()
            res.saveResults(f'{out_dir}{self.name}{self.removed_phase}.res')
        #self.save_results(self, out_dir, name_ext=self.removed_phase)






