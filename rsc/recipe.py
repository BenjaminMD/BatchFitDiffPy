from diffpy.srfit.fitbase import FitResults
from diffpy.srfit.pdf import PDFParser
from rsc.fitconfig import FitConfig
from itertools import count
import rsc.diffpyhelper as dh


class CreateRecipe():
    def __init__(self, conf, phases, char_function):
        self.conf = FitConfig(**conf)
        # self.data_file = data_file
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
        for phase, function in zip(self.phases, self.char_function):
            function_definition = self.conf.fetch_function(phase, function)
            self.functions[f'{phase}{function}'] = function_definition

    def update_recipe(self):
        self.recipe = dh.create_recipe_from_files(
            # data_file=self.data_file,
            meta_data=self.conf(),
            equation=self.equation,
            cif_files=self.cif_files,
            functions=self.functions
        )

    def update_data(self, data_file):
        if not hasattr(self, 'recipe'):
            self.update_recipe()
        pp = PDFParser()
        pp.parseFile(data_file)
        profile = self.recipe._contributions['PDF'].profile
        profile.loadParsedData(pp)
        profile.meta.update(self.conf())

    def default_restraints(self):
        recipe = self.recipe
        for phase in self.phases:

            delta2 = getattr(self.recipe, f'{phase}_delta2')
            recipe.restrain(delta2, lb=1, ub=5, sig=1e-3)
            delta2.value = 3.0

            scale = getattr(self.recipe, f'{phase}_scale')
            recipe.restrain(scale, lb=0.01, ub=2, sig=1e-3)
            scale.value = 0.5

            for abc in ['a', 'b', 'c']:
                try:
                    lat = getattr(self.recipe, f'{phase}_{abc}')
                    lb_lat = lat.value - 0.2
                    ub_lat = lat.value + 0.2
                    recipe.restrain(lat, lb=lb_lat, ub=ub_lat, sig=1e-3)
                except AttributeError:
                    pass

            for func in self.functions.values():
                params = func[1][1:]
                for p in params:
                    param = getattr(self.recipe, p)
                    recipe.restrain(param, lb=0, ub=1e2, sig=1e-3)

    def create_param_order(self):
        ns = []
        for phase in self.phases:
            for func in self.functions.values():
                for varn in func[1][1:]:
                    ns.append(varn)
        ns = [n for n in ns if n]
        self.param_order = [
            ['free', 'lat', 'scale'],
            ['free', *ns],
            ['free', 'adp', 'delta2'],
        ]
