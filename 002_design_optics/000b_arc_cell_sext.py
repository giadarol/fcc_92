import xtrack as xt
import numpy as np

env = xt.Environment()
env.call('../fccee_z_lattice.py')
env.call('quad_strength_limits.py')

env.call('matching_constraints.py')

# Load cell strengths from previous match
env.vars.load_json('strengths_quads_00_arc_cell.json')

line = env['cell_u']

tt0 = line.get_table(attr=True)
tt0_quad = tt0.rows[tt0.element_type == 'Quadrupole']
tt0_sext = tt0.rows[tt0.element_type == 'Sextupole']

ks = {}
ks['cell'] = ['ksffam1', 'ksffam2', 'ksdfam1', 'ksdfam2']

# Build vary objects keeping the initial signs
vary_ks = {}
for kk in ks.keys():
    vary_ks[kk] = []
    for nn in ks[kk]:
        vary_ks[kk].append(xt.Vary(nn, step=1e-4, tag=kk))
vary_all = []
for kk in ks.keys():
    vary_all += vary_ks[kk]

# Redefine sextupole circuits
env.vars.default_to_zero = True
env['ksf1'] = 'ksffam1'
env['ksf2'] = 'ksffam2'
env['ksf3'] = 'ksffam1'
env['ksf4'] = 'ksffam2'
env['ksd1'] = 'ksdfam1'
env['ksd2'] = 'ksdfam2'
env['ksd3'] = 'ksdfam1'
env['ksd4'] = 'ksdfam2'
env.vars.default_to_zero = False

tar_chrom = xt.TargetSet(dqx=env['dqx_cell'], dqy=env['dqy_cell'], tol=1e-3)

# Match chromaticity
opt_chrom = line.match(
    name='linear chromaticity',
    solve=False,
    method='4d',
    vary=vary_ks['cell'],
    targets=tar_chrom
)
opt = opt_chrom
opt.step(20)
tw_chrom = line.twiss4d(strengths=True)

line_starfish = 3*120 * env['cell_u']

# Put the fractional tune on 0.2
opt_tune_star = line_starfish.match(
    name='tune for starfish',
    solve=False,
    method='4d',
    vary=xt.VaryList(['kqd1', 'kqf2', 'kqd3', 'kqf4', 'kqd5', 'kqf6'], step=1e-6),
    targets=xt.TargetSet(qx=254.2, qy=222.2)
)
opt = opt_tune_star
opt.step(20)


nemitt_x=1e-7
nemitt_y=1e-8
n_test = 10

from starfish import Starfish
starfish = Starfish(line_starfish, nemitt_x=nemitt_x, nemitt_y=nemitt_y, n_test=n_test)

opt_starfish = line.match(
    name='starfish',
    solve=False,
    method='4d',
    vary=vary_ks['cell'],
    targets=[tar_chrom,
             starfish.target('px_norm_rms_5', 0),
             starfish.target('pxy_norm_rms_5', 0)]
)
opt = opt_starfish
opt.step(10)

out = {}
sext_strengths = ['ksf1', 'ksf2', 'ksf3', 'ksf4',
                  'ksd1', 'ksd2', 'ksd3', 'ksd4']
out.update(env.vars.get_table().rows[sext_strengths].to_dict())
out.update(opt_starfish.get_knob_values(-1))

import json
with open('strengths_sext_00_arc_cell.json', 'w') as fid:
    json.dump(out, fid, indent=2)

import matplotlib.pyplot as plt
plt.close('all')
opt_starfish.reload(-1)
sf2 = starfish(plot=True)
plt.suptitle('After optimization')

opt_chrom.reload(-1)
sf1 = starfish(plot=True)
plt.suptitle('Only chromaticity correction')


plt.show()
