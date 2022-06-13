from diffpy.srfit.fitbase import FitResults
from fitconfig import FitConfig
from itertools import count
import diffpy_wrap as dw


class RecipeClass(FitConfig):
    def __init__(self, file, phases, char_function):
        self.file = file
        self.phases = self._parse_phases(phases)
        self.char_function = char_function

        self.create_cif_files()
        self.create_equation()
        self.create_functions()

    def _phase_counter(self, phase):
        if not hasattr(self, f'{phase}_count'):
            setattr(self, f'{phase}_count', count(1))
            return 0
        else:
            return next(getattr(self, f'{phase}_count'))

    def _parse_phases(self, phases):
        phases_cp = phases.copy()
        for i, phase in enumerate(phases):
            ocur = phases.count(phase)
            # if ocur < 1:
            #     continue
            # cnt = self._phase_counter(phase)
            # phases_cp[i] = f'{phase}Γ{cnt}'
            if ocur > 1:
                cnt = self._phase_counter(phase)
                phases_cp[i] = f'{phase}Γ{cnt}'

        return phases_cp

    def create_cif_files(self):
        self.cif_files = {}
        for phase in list(self.phases):
            self.cif_files[f'{phase}'] = f'./CIFS/{phase.split("Γ")[0]}.cif'

    def create_equation(self):
        equation_list = []
        for phase, function in zip(self.phases, self.char_function):
            equation_list.append(f'{phase} * {phase}{function}')
        self.equation = ' + '.join(equation_list)

    def create_functions(self):
        self.functions = {}
        for phase, function in zip(self.phases, self.nano_shape):
            function_definition = FitConfig().fetch_function(phase, function)
            self.functions[f'{phase}{function}'] = function_definition

    def update_recipe(self):
        self.recipe = dw.create_recipe_from_files(
            data_file=self.file,
            meta_data=FitConfig()(),
            equation=self.equation,
            cif_files=self.cif_files,
            functions=self.functions
        )

    def update_data(self):
        # profile parser