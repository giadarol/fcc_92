import numpy as np
import xtrack as xt
from xtrack.mad_parser.parse import MadxParser
from xtrack.mad_parser.loader import MadxLoader, get_params

parser = MadxParser()
loader = MadxLoader()

fname = '../fcc-ee-lattice/lattices/z/fccee_z.seq'

with open(fname, 'r') as fid:
    lines = fid.readlines()

# Remove lines containing the "LINE" command (not yet implemented)
lines = [ll for ll in lines if 'LINE=' not in ll.replace(' ', '')]

# Patch: issue with power
for ii, ll in enumerate(lines):
    if ll.startswith('KCRABL'):
        lines[ii] = 'KCRABL=0.0;\n'

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

other = set(list(tt_elements.name))
for pp in tt_ele_dct:
    other = other.difference(set(list(tt_ele_dct[pp].name)))

assert len(other) == 0

out_lattice = []
out_lattice.append('import xtrack as xt')
out_lattice.append('env = xt.get_environment()')
out_lattice.append('env.vars.default_to_zero=True')
out_lattice.append('')

BASE_TYPE_DEFS = '''
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
out_lattice.append(BASE_TYPE_DEFS)

for pp in ele_types:
    if len(tt_ele_dct[pp]) == 0:
        continue
    out_lattice.append(f'# {pp} elements:')
    for nn in tt_ele_dct[pp].name:
        out_lattice.append(tt_elements['element_defs', nn])
    out_lattice.append('')

out_lattice.append('env.vars.default_to_zero=False')

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

tt_strengths = tt_vars.rows['k.*']
other = sorted(list(set(list(tt_vars.name)) - set(list(tt_strengths.name))))
tt_other = tt_vars.rows[other]

out_strengths = []
out_strengths.append('import xtrack as xt')
out_strengths.append('env = xt.get_environment()')
out_strengths.append('env.vars.default_to_zero=True')
out_strengths.append('')
for nn in sorted(list(tt_strengths.name)):
    ee = tt_vars['expr', nn]
    if isinstance(ee, str):
        out_strengths.append(f'env["{nn}"] = "{ee}"')
    else:
        out_strengths.append(f'env["{nn}"] = {ee}')
out_strengths.append('')
out_strengths.append('env.vars.default_to_zero=False')

out_other = []
out_other.append('import xtrack as xt')
out_other.append('env = xt.get_environment()')
out_other.append('env.vars.default_to_zero=True')
out_other.append('')
for nn in sorted(list(tt_other.name)):
    ee = tt_vars['expr', nn]
    if isinstance(ee, str):
        out_other.append(f'env["{nn}"] = "{ee}"')
    else:
        out_other.append(f'env["{nn}"] = {ee}')
out_other.append('')
out_other.append('env.vars.default_to_zero=False')

with open('fccee_z.py', 'w') as fid:
    fid.write('\n'.join(out_lattice))

with open('fccee_z_strengths.py', 'w') as fid:
    fid.write('\n'.join(out_strengths))

with open('fccee_z_parameters.py', 'w') as fid:
    fid.write('\n'.join(out_other))

