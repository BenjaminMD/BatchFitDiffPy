import json


def read_config(config_path):
    with open(config_path) as f:
        dat = json.load(f)
    return dat

# def remove_phase(self, p):
#     if p not in self.phases:
#         raise ValueError(f'{p} is not in phases')
#     self.phases.remove(p)

#     f = self.p_f[p]

#     # remove phase from equation
#     equation_list = self.equation.split(' + ')
#     equation_list.remove(f'{p}Γ * {p}Γ{f}')
#     self.equation = ' + '.join(equation_list)

#     # remove phase from cif_files
#     self.cif_files.pop(f'{p}Γ')

#     # remove phase from functions
#     self.functions.pop(f'{p}Γ{f}')

# def add_phase(self, p):
#     if p in self.phases:
#         raise ValueError(f'{p} is already in phases')
#     self.phases.append(p)
#     f = self.p_f[p]

#     # add phase to equation
#     equation_list = self.equation.split(' + ')
#     equation_list.append(f'{p}Γ * {p}Γ{f}')
#     self.equation = ' + '.join(equation_list)

#     # add phase to cif_files
#     self.cif_files[f'{p}Γ'] = f'{p}.cif'

#     # add phase to functions
#     self.functions[f'{p}Γ{f}'] = self.fetch_function(p ,self.p_f[p])
