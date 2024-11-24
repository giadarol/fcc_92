import xtrack as xt
import numpy as np

env = xt.Environment()
env.call('../fccee_z_lattice.py')
env.call('quad_strength_limits.py')

env.call('matching_constraints.py')

line = env['cell_u']

tt0 = line.get_table(attr=True)
tt0_quad = tt0.rows[tt0.element_type == 'Quadrupole']
tt0_sext = tt0.rows[tt0.element_type == 'Sextupole']


kq = {}
kq['cell'] = ['kqd1', 'kqf2', 'kqd3', 'kqf4', 'kqd5', 'kqf6']

# Build vary objects keeping the initial signs
vary_kq = {}
for kk in kq.keys():
    vary_kq[kk] = []
    for nn in kq[kk]:
        vary_kq[kk].append(xt.Vary(nn, step=1e-6, tag=kk))

vary_all = []
for kk in kq.keys():
    vary_all += vary_kq[kk]

tar_mu = xt.TargetSet(at=xt.END, mux=env['muxu'], muy=env['muyu'])
tar_dx = xt.Target(
    lambda tw: tw.rows['qf.*']['dx'].std(), xt.LessThan(0.001), tag='dx', weight=1000)
tar_betx = xt.Target(
    lambda tw: tw.rows['qf.*']['betx'].std(), xt.LessThan(0.1), tag='betx')
tar_bety = xt.Target(lambda tw: tw.rows[['qd3a::0', 'qd5a::0', 'qd5a::1', 'qd3a::1', 'qd1a::1']]['bety'].std(),
                     xt.LessThan(0.1), tag='bety')

# Put a small strength on quadrupoles
for kk in kq['cell']:
    if env.vars.vary_default[kk]['limits'][0] == 0:
        env[kk] = 0.01
    else:
        env[kk] = -0.01

opt_quads = line.match(
    solve=False,
    method='4d',
    vary=vary_kq['cell'],
    targets=[tar_mu, tar_betx, tar_bety, tar_dx]
)
opt = opt_quads
opt.step(10)
opt.run_simplex(100)
opt.step(20)
opt.run_simplex(100, xatol=1e-8, fatol=1e-10)
opt.disable(target='bet.*')
opt.step(20)

import json
with open('strengths_quads_00_arc_cell.json', 'w') as fid:
    json.dump(opt_quads.get_knob_values(-1), fid)
