from diffpy.srfit.fitbase import FitResults
from rsc.recipe import CreateRecipe
import rsc.diffpyhelper as dh
import numpy
import re 

class DiffpyFit(CreateRecipe):
    def __init__(self, conf, phases, char_function):
        super().__init__(conf, phases, char_function)

    def run_simple_fit(self, data_file, out_dir):
        self.name = data_file.split('/')[-1].split('.')[0]
        if not hasattr(self, 'recipe'):
            self.update_data(data_file)
            self.update_recipe()
            self.default_restraints()
            self.create_param_order()

        else:
            self.update_data(data_file)
        # self.complete_recipe(data_file)
        dh.optimize_params_manually(
            self.recipe,
            self.param_order,
            rmin=self.conf.rmin,
            rmax=self.conf.rmax,
            rstep=self.conf.rstep,
            ftol=1e-5,
            print_step=False
        )
        dh.save_results(self.recipe, './out/', self.name, self.phases)
        self.save_fits('./out/')
        #res = FitResults(self.recipe)
        #res.saveResults(f'{out_dir}{self.name}.res')

    def get_gr(self, recipe):
        """
        Get the gr of a recipe and for each phase contribution
        returns:
        - r: list of floats
        - gobs: list of floats
        - gcalc: list of floats
        - gdiff: list of floats
        - baseline: float 
        - gr_composition: dict of list of floats
        """
        def remove_consecutive_duplicates(string, char):
            indices = [m.start() for m in re.finditer(char * 2, string)]
            if indices:
                for i in indices:
                    string = string[:i] + string[i+1:]
                return remove_consecutive_duplicates(string, char)
            else:
                return string

        equation = recipe.PDF.getEquation()        
        for char in ['\)', '\(']:
            equation = (remove_consecutive_duplicates(equation, char))
    

        prof = recipe._contributions['PDF'].profile
        r = prof.x
        gobs = prof.y
        gcalc = recipe._contributions['PDF'].evaluate()
        baseline = 1.35 * gobs.min()
        gdiff = gobs - gcalc


        gr_composition = {}
        for eq in equation.split(' + '):
            gr = recipe.PDF.evaluateEquation(eq[1:])
            gr_composition[eq[1:]] = gr

        return r, gobs, gcalc, gdiff, baseline, gr_composition


    def save_results(self, out_dir, name_ext=''):
        #self.recipe.show()
        res = FitResults(self.recipe)
        res.saveResults(f'{out_dir}{self.name}{name_ext}.res')

    def save_fits(self, out_dir, name_ext=''):
        r, gobs, gcalc, gdiff, baseline, gr_composition = self.get_gr(self.recipe)

        dat = [v for v in gr_composition.values()]
        dataout = numpy.column_stack([r, gobs, gcalc, gdiff, *dat])
        numpy.savetxt(f'{out_dir}{self.name}{name_ext}.fit', dataout)

    def complete_recipe(self, data_file):
        self.update_recipe()
        self.update_data(data_file)
        self.create_param_order()
        self.default_restraints()
        
        

    def run_molarcontribution_fit(self, data_file, out_dir, molar_limit):
        self.complete_recipe(data_file)
        self.run_simple_fit(data_file, out_dir)

        self.removed_phase = []
        for phase in self.phases:
            mol_contrib = self.get_mol_contribution(phase)
            #print(f'{phase} scale: {mol_contrib}')
            
            if mol_contrib < molar_limit:
                self.remove_phase(phase)
                self.removed_phase.append(phase)


                self.complete_recipe(data_file)
                self.run_simple_fit(data_file, out_dir)


        if self.removed_phase:
            [self.add_phase(phase) for phase in self.removed_phase]
            
        
        self.update_data(data_file)
        self.name = data_file.split('/')[-1].split('.')[0]
        self.save_results(out_dir, name_ext=self.removed_phase)







