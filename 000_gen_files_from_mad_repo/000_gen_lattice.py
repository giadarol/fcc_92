import numpy as np
import xtrack as xt
import xdeps as xd
from xtrack.mad_parser.parse import MadxParser
from xtrack.mad_parser.loader import CONSTANTS

formatter = xd.refs.CompactFormatter(scope=None)
SKIP_PARAMS = ['order', 'model', '_edge_entry_model', '_edge_exit_model',
               'h',
               'k0' # we assume that k0 is always equal to h
]


def _repr_arr_ref(arr_ref, formatter):
    out = []
    for ii, vv in enumerate(arr_ref._value):
        if arr_ref[ii]._expr is not None:
            out.append(f'"{arr_ref[ii]._expr._formatted(formatter)}"')
        else:
            out.append(f'{arr_ref[ii]._value:g}')

    # Trim trailing zeros
    while out and (out[-1] == '0' or out[-1] == '-0'):
        out.pop()

    return f'[{", ".join(out)}]'

def _elem_to_tokens(env, nn, formatter):

    ee = env.get(nn)
    ee_ref = env.ref[nn]

    # The fields to consider are those in the dictionary, plus knl and ksl, plus
    # anything that has an expression
    fields = list(ee.to_dict().keys())
    if hasattr(ee, 'knl'):
        fields += ['knl']
    if hasattr(ee, 'ksl'):
        fields += ['ksl']

    tt = env[nn].get_table()
    for kk in tt.name:
        if tt['expr', kk] is not None and tt['expr', kk] != 'None':
            fields.append(kk)

    params = []
    for kk in fields:
        if kk == '__class__':
            continue
        if kk in SKIP_PARAMS:
            continue
        if kk == 'knl' or kk == 'ksl':
            arr_ref = getattr(ee_ref, kk)
            vv = _repr_arr_ref(arr_ref, formatter)
            if vv != '[]':
                params.append(f'{kk}={vv}')
        elif getattr(ee_ref, kk)._expr is not None:
            params.append(f'{kk}="{getattr(ee_ref, kk)._expr._formatted(formatter)}"')
        else:
            params.append(f'{kk}={getattr(ee_ref, kk)._value:g}')

    out = {'name': nn, 'element_type': ee.__class__.__name__, 'params': params,
           'prototype': getattr(ee, 'prototype', None),
           'extra': getattr(ee, 'extra', None)}
    return out

fname = '../../fcc-ee-lattice/lattices/z/fccee_z.seq'
env = xt.load_madx_lattice(fname)

# Impose RF frequency (in madx it is defined by harmon, not supported by xtrack)
env['f_rev'] = 3306.828357898286
env['harmonic_number'] = 121200
env['rfc'].frequency = 'harmonic_number * f_rev'

###################
# Handle elements #
###################

all_elems = []
for lname in env.lines.keys():
    ll = env.lines[lname]
    bb = ll.builder.flatten()
    all_elems += [cc.name for cc in bb.components]

elem_tokens = {}
for nn in all_elems:
    elem_tokens[nn] = _elem_to_tokens(env, nn, formatter)

while True:
    added = False
    for nn in list(elem_tokens.keys()):
        if elem_tokens[nn]['prototype'] is not None:
            parent_name = elem_tokens[nn]['prototype']
            if parent_name not in elem_tokens:
                elem_tokens[parent_name] = _elem_to_tokens(env, parent_name, formatter)
                added = True
    if not added:
        break

# Some customizations
elem_tokens['multipole']['params'].append('knl=[0,0,0,0,0,0]')

# remove length when length_straight is present
for nn in elem_tokens:
    if 'length_straight' in elem_tokens[nn]['params']:
        elem_tokens[nn]['params'] = [pp for pp in elem_tokens[nn]['params'] if pp != 'length']

# populate diff params
for nn in elem_tokens:
    diff_params = []
    if elem_tokens[nn]['prototype'] is not None:
        parent_name = elem_tokens[nn]['prototype']
        parent_params = elem_tokens[parent_name]['params']
        elem_params = set(elem_tokens[nn]['params'])
        for pp in elem_params:
            if pp not in parent_params:
                diff_params.append(pp)
    else:
        diff_params = elem_tokens[nn]['params']
    elem_tokens[nn]['diff_params'] = diff_params

# Build def instruction
for nn in elem_tokens:
    out_parts = []
    out_parts.append(f'env.new("{nn}"')
    if elem_tokens[nn]['prototype'] is not None:
        out_parts.append(f'"{elem_tokens[nn]["prototype"]}"')
    else:
        out_parts.append(f'"{elem_tokens[nn]["element_type"]}"')
    if len(elem_tokens[nn]['diff_params']) > 0:
        out_parts += elem_tokens[nn]['diff_params']
    if elem_tokens[nn]['extra'] is not None:
        out_parts.append(f'extra={elem_tokens[nn]["extra"]}')
    elem_tokens[nn]['def_instruction'] = ', '.join(out_parts) + ')'

# Sort based on hierarchy
sorted_elems = []
def _add_elem(nn):
    if elem_tokens[nn]['prototype'] is not None:
        _add_elem(elem_tokens[nn]['prototype'])
    if nn not in sorted_elems:
        sorted_elems.append(nn)
for nn in elem_tokens:
    _add_elem(nn)

tt_edefs = xt.Table({
    'name': np.array(sorted_elems),
    'element_type': np.array([elem_tokens[nn]['element_type'] for nn in sorted_elems]),
    'prototype': np.array([elem_tokens[nn]['prototype'] for nn in sorted_elems]),
    'def_instruction': np.array([elem_tokens[nn]['def_instruction'] for nn in sorted_elems]),
})

tt_gen0 = tt_edefs.rows[tt_edefs['prototype'] == None]
tt_gen0.gen_name = 'Xsuite types'

generation_tree = [{'Xsuite types': tt_gen0}]
while True:
    print(f'Generation {len(generation_tree)}')
    last_gen = generation_tree[-1]
    names_last_gen = []
    for nn in last_gen.keys():
        names_last_gen += list(last_gen[nn]['name'])
    this_gen = {}
    added = False
    for nn in names_last_gen:
        tt_gen = tt_edefs.rows[tt_edefs['prototype'] == nn]
        if len(tt_gen) > 0:
            tt_gen.gen_name = nn
            this_gen[nn] = tt_gen
            added = True
    if added:
        generation_tree.append(this_gen)
    else:
        break

# Flatten generations
generations = []
for gg in generation_tree:
    for nn in gg.keys():
        generations.append(gg[nn])

# Build elem def part (with generations)
elem_def_lines = []
for tt_gen in generations:
    elem_def_lines.append(f'\n# Elements of type: {tt_gen.gen_name}')
    for nn in tt_gen.name:
        elem_def_lines.append(elem_tokens[nn]['def_instruction'])

elem_def_part = '\n'.join(elem_def_lines)

####################
# Handle variables #
####################

ttvars = env.vars.get_table()
const = set(CONSTANTS.keys())
lattice_parameters = [nn for nn in ttvars.name if nn not in const]

tt_lattice_pars_all = ttvars.rows[lattice_parameters]
mask_keep = (
    ((tt_lattice_pars_all['expr'] != None) | (tt_lattice_pars_all['value'] != 0))
    & (tt_lattice_pars_all['name'] != '__temp__'))
tt_lattice_pars = tt_lattice_pars_all.rows[mask_keep]

statement = []
for nn in tt_lattice_pars.name:
    if tt_lattice_pars['expr', nn] is not None:
        statement.append(f'env["{nn}"] = "{tt_lattice_pars["expr", nn]}"')
    else:
        statement.append(f'env["{nn}"] = {tt_lattice_pars["value", nn]}')
tt_lattice_pars['statement'] = np.array(statement)

# Separate strengths
mask_strengths = tt_lattice_pars.rows.mask['k.*']
tt_strengths = tt_lattice_pars.rows[mask_strengths]
tt_lattice_other_pars = tt_lattice_pars.rows[~mask_strengths]

strengths_part = '\n'.join(tt_strengths['statement'])
other_lattice_pars_part = '\n'.join(tt_lattice_other_pars['statement'])

######################
# Lattice definition #
######################

with open('_part_description.py', 'r') as fid:
    part_description = fid.read()

with open('_part_lattice.py', 'r') as fid:
    part_lattice = fid.read()


##########################
# Models and integrators #
##########################

model_integ_part = '''
tt = env.fccee_p_ring.get_table()
tt_bend = tt.rows[(tt.element_type=='Bend') | (tt.element_type=='RBend')]
tt_quad = tt.rows[(tt.element_type=='Quadrupole')]
tt_sext = tt.rows[(tt.element_type=='Sextupole')]

env.set(tt_bend, integrator='uniform', num_multipole_kicks=3, model='mat-kick-mat')
env.set(tt_quad, integrator='uniform', num_multipole_kicks=3, model='mat-kick-mat')
env.set(tt_sext, integrator='yoshida4', num_multipole_kicks=1)
'''


#####################
# Assemble the file #
#####################

preamble = '''import xtrack as xt
env = xt.get_environment()
env.vars.default_to_zero=True
'''

# Reference particle
lines_ref_particle = [
    '# Reference particle',
    'env.particle_ref = xt.Particles(mass0=xt.ELECTRON_MASS_EV, energy0=45.6e9)'
]
part_ref_particle = '\n'.join(lines_ref_particle)


postamble = '''

env.vars.default_to_zero=False

'''

file_content = '\n'.join([
    preamble,
    part_description,
    part_ref_particle,
   '',
   '#############',
   '# Variables #',
   '#############',
   '',
   other_lattice_pars_part,
   '############',
   '# Elements #',
   '############',
   elem_def_part,
   '',
   '##############',
   '# Beam lines #',
   '##############',
   '',
   part_lattice,
    '',
   '##########################',
   '# Models and integrators #',
   '##########################',
   '',
   model_integ_part,
   '',
   postamble])

with open('fccee_z_lattice.py', 'w') as ff:
    ff.write(file_content)

out_strengths = '\n'.join(
    [preamble, strengths_part, postamble]
)
with open('fccee_z_strengths.py', 'w') as ff:
    ff.write(out_strengths)

# Copy lattice and strengths to the main directory
import shutil
shutil.copy('fccee_z_lattice.py', '..')
shutil.copy('fccee_z_strengths.py', '..')