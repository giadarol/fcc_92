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
        ee_def_tokens.append(f"{pp}={vv}")
    ee_def = 'env.new(' + ', '.join(ee_def_tokens) + ')'
    element_defs.append(ee_def)

tt_elements = xt.Table({
    'name': np.array(name),
    'parent': np.array(parent),
    'element_defs': np.array(element_defs),
})

tt_marker = tt_elements.rows[tt_elements.parent == 'marker']
tt_sbend = tt_elements.rows[tt_elements.parent == 'sbend']
tt_rbend = tt_elements.rows[tt_elements.parent == 'rbend']
tt_quad = tt_elements.rows[tt_elements.parent == 'quadrupole']
tt_sext = tt_elements.rows[tt_elements.parent == 'sextupole']
tt_octu = tt_elements.rows[tt_elements.parent == 'octupole']
tt_mult = tt_elements.rows[tt_elements.parent == 'multipole']
tt_drift = tt_elements.rows[tt_elements.parent == 'drift']
tt_cav = tt_elements.rows[tt_elements.parent == 'rfcavity']

other = set(list(tt_elements.name)) - set(
    list(tt_marker.name) +
    list(tt_sbend.name) + list(tt_rbend.name) +
    list(tt_quad.name) + list(tt_sext.name) +
    list(tt_octu.name) + list(tt_mult.name) +
    list(tt_drift.name) + list(tt_cav.name))

assert len(other) == 0

out_lattice = []
out_lattice.append('import xtrack as xt')
out_lattice.append('env = xt.get_environment()')
out_lattice.append('')
out_lattice.append('###########')
out_lattice.append('# Markers #')
out_lattice.append('###########')
