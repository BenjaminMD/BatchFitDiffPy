from diffpy.srfit.fitbase import FitResults
from diffpy.srfit.pdf import PDFParser
from fitconfig import FitConfig
from itertools import count
import diffpyhelper as dh


class CreateRecipe():
    def __init__(self, conf, data_file, phases, char_function):
        self.conf = FitConfig(**conf)
        self.data_file = data_file
        self.char_function = char_function

        self.phases = self._parse_phases(phases)

        self._create_cif_files()
        self._create_equation()
        self._create_functions()

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

    def _create_cif_files(self):
        self.cif_files = {}
        for phase in list(self.phases):
            self.cif_files[f'{phase}'] = f'./CIFS/{phase.split("Γ")[0]}.cif'

    def _create_equation(self):
        equation_list = []
        for phase, function in zip(self.phases, self.char_function):
            equation_list.append(f'{phase} * {phase}{function}')
        self.equation = ' + '.join(equation_list)

    def _create_functions(self):
        self.functions = {}
        for phase, function in zip(self.phases, self.nano_shape):
            function_definition = FitConfig().fetch_function(phase, function)
            self.functions[f'{phase}{function}'] = function_definition

    def update_recipe(self):
        self.recipe = dh.create_recipe_from_files(
            data_file=self.data_file,
            meta_data=self.conf(),
            equation=self.equation,
            cif_files=self.cif_files,
            functions=self.functions
        )

    def update_data(self, data_file):
        if not self.recipe:
            self.update_recipe()
        pp = PDFParser()
        pp.parseFile(data_file)
        profile = self.recipe._contributions['PDF'].profile
        profile.loadParsedData(pp)
        profile.meta.update(self.conf())
