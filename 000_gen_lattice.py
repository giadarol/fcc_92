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
out_lattice.append('')

for pp in ele_types:
    if len(tt_ele_dct[pp]) == 0:
        continue
    out_lattice.append(f'# {pp} elements:')
    for nn in tt_ele_dct[pp].name:
        out_lattice.append(tt_elements['element_defs', nn])
    out_lattice.append('')

with open('fccee_z.py', 'w') as fid:
    fid.write('\n'.join(out_lattice))

