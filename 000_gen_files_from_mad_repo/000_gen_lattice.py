import numpy as np
import xtrack as xt
from xtrack.mad_parser.parse import MadxParser
from xtrack.mad_parser.loader import MadxLoader, get_params

parser = MadxParser()
loader = MadxLoader()

fname = '../../fcc-ee-lattice/lattices/z/fccee_z.seq'

with open(fname, 'r') as fid:
    lines = fid.readlines()

# Remove lines containing the "LINE" command (not yet implemented)
lines = [ll for ll in lines if 'LINE=' not in ll.replace(' ', '')]

# Patch: issue with power
# for ii, ll in enumerate(lines):
#     if ll.startswith('KCRABL'):
#         lines[ii] = 'KCRABL=0.0;\n'

dct = parser.parse_string('\n'.join(lines))
loader.load_string('\n'.join(lines))

elements = dct['elements']
element_defs = []
name = []
parent = []
for nn, el_params in elements.items():

    par = el_params.pop('parent')
    assert par != 'sequence'
    parent.append(par)
    name.append(nn)

    params, extras = get_params(el_params, parent=par)
    el_params = loader._pre_process_element_params(nn, params)

    # PATCH!!!!
    if par in ['sbend', 'rbend']:
        el_params['k0_from_h'] = True

    ee_def_tokens = []
    ee_def_tokens.append(f"'{nn}'")
    ee_def_tokens.append(f"'{par}'")
    for pp, vv in el_params.items():
        if isinstance(vv, str):
            ee_def_tokens.append(f"{pp}='{vv}'")
        else:
            ee_def_tokens.append(f"{pp}={vv}")
    ee_def = 'env.new(' + ', '.join(ee_def_tokens) + ')'
    element_defs.append(ee_def)

tt_elements = xt.Table({
    'name': np.array(name),
    'parent': np.array(parent),
    'element_defs': np.array(element_defs),
})

tt_ele_dct ={}

ele_types = ['marker', 'sbend', 'rbend', 'quadrupole', 'sextupole',
           'octupole', 'multipole', 'drift', 'rfcavity']

for pp in ele_types:
    tt_ele_dct[pp] = tt_elements.rows[tt_elements.parent == pp]

parameters = set(list(tt_elements.name))
for pp in tt_ele_dct:
    parameters = parameters.difference(set(list(tt_ele_dct[pp].name)))

assert len(parameters) == 0

at_start_file = []
at_start_file.append('import xtrack as xt')
at_start_file.append('env = xt.get_environment()')
at_start_file.append('env.vars.default_to_zero=True')
at_start_file.append('')

at_end_file = []
at_end_file.append('env.vars.default_to_zero=False')
at_end_file.append('')

BASE_TYPE_DEFS = '''
# Base types
env.new("sbend", "Bend")
env.new("rbend", "Bend", rbend=True)
env.new("quadrupole", "Quadrupole")
env.new("sextupole", "Sextupole")
env.new("octupole", "Octupole")
env.new("marker", "Marker")
env.new("rfcavity", "Cavity")
env.new("multipole", "Multipole", knl=[0, 0, 0, 0, 0, 0])
env.new("solenoid", "Solenoid")
env.new("drift", "Drift")
'''

out_elements = []
out_elements.append(BASE_TYPE_DEFS)
for pp in ele_types:
    if len(tt_ele_dct[pp]) == 0:
        continue
    out_elements.append(f'# {pp} elements:')
    for nn in tt_ele_dct[pp].name:
        out_elements.append(tt_elements['element_defs', nn])
    out_elements.append('')

## Variables
variables = dct['vars']
v_names = []
v_expr = []
for nn, vv in variables.items():
    v_names.append(nn)
    v_expr.append(vv['expr'])

tt_vars = xt.Table({
    'name': np.array(v_names),
    'expr': np.array(v_expr),
})

# Identify expressions
env_vars = xt.Environment()
env_vars.vars.default_to_zero = True
for nn in tt_vars.name:
    env_vars[nn] = tt_vars['expr', nn]
tt_env_vars = env_vars.vars.get_table()
is_expr = [(tt_env_vars['expr', nn] is not None) for nn in tt_vars.name]
tt_vars['is_expr'] = np.array(is_expr)

out_statement = []
for nn in tt_vars.name:
    if tt_vars['is_expr', nn]:
        out_statement.append(f'env["{nn}"] = "{tt_vars["expr", nn]}"')
    else:
        out_statement.append(f'env["{nn}"] = {tt_vars["expr", nn]}')

tt_vars['statement'] = np.array(out_statement)


tt_strengths = tt_vars.rows['k.*']
parameters = sorted(list(set(list(tt_vars.name)) - set(list(tt_strengths.name))))
tt_other = tt_vars.rows[parameters]


out_strengths = []
for nn in sorted(list(tt_strengths.name)):
    out_strengths.append(tt_strengths['statement', nn])

out_other = []
for nn in sorted(list(tt_other.name)):
    out_other.append(tt_other['statement', nn])

with open('_tmp_elements.py', 'w') as fid:
    fid.write('\n'.join(
        at_start_file + out_elements + at_end_file))

with open('_tmp_parameters.py', 'w') as fid:
    fid.write('\n'.join(
        at_start_file + out_other + at_end_file))

# Separate lattice parameters from other parameters
env = xt.Environment()
env.call('_tmp_elements.py')
env.call('_tmp_parameters.py')

lattice_parameters = []
for nn in tt_other.name:
    if 'element_refs' in str(env.ref[nn]._find_dependant_targets()):
        lattice_parameters.append(nn)

out_lattice_parameters = []
for nn in lattice_parameters:
    out_lattice_parameters.append(tt_other['statement', nn])

with open('_part_description.py', 'r') as fid:
    part_description = [fid.read()]

with open('_part_lattice.py', 'r') as fid:
    part_lattice = [fid.read()]

# RF frequency
out_rf_frequency = [
    '# RF frequency',
    'env["rfc"].frequency = 121200*3306.828357898286'
]



with open('fccee_z_lattice.py', 'w') as fid:
    fid.write('\n'.join(
        part_description +
        [''] +
        at_start_file +
        ['# Lattice parameters:'] +
        out_lattice_parameters +
        out_elements +
        out_rf_frequency +
        [''] +
        ['# Ring sections:'] +
        part_lattice +
        at_end_file))

with open('fccee_z_strengths.py', 'w') as fid:
    fid.write('\n'.join(
        at_start_file + out_strengths + at_end_file))

other_parameters = sorted(list(
                          set(list(tt_vars.name))
                        - set(lattice_parameters)
                        - set(list(tt_strengths.name))))
out_other_parameters = []
for nn in other_parameters:
    out_other_parameters.append(tt_vars['statement', nn])

with open('fccee_z_other_parameters.py', 'w') as fid:
    fid.write('\n'.join(
        at_start_file +
        ['# Other parameters:'] +
        out_other_parameters +
        at_end_file))

# Copy lattice and strengths to the main directory
import shutil
shutil.copy('fccee_z_lattice.py', '..')
shutil.copy('fccee_z_strengths.py', '..')