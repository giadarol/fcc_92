import numpy as np
import xtrack as xt

env = xt.Environment()
env.call('../fccee_z_lattice.py')
env.call('quad_strength_limits.py')

env.call('matching_constraints.py')

# Load cell strengths from my match
env.vars.load_json('strengths_quads_00_arc_cell.json')

tw_uu = (2 * env['cell_u']).twiss4d()

# Full service straight with dispersion suppressors
line = (env['cell_us'] + env['straight_l']
                   + (-env['straight_r']) + (-env['cell_su']))

kq = {}
kq['ussu'] = [
    'kqfs0', 'kqds0', 'kqfs1', 'kqds2', 'kqfs3', 'kqds4',
    'kqfs5', 'kqdl1', 'kqfl2', 'kqdl2', 'kqfl3', 'kqdl3',
    'kqfl6', 'kqdl4', 'kqfl4', 'kqfl5', 'kqdl5', 'kqdl6']

# Build vary objects keeping the initial signs
vary_kq = {}
for kk in kq.keys():
    vary_kq[kk] = []
    for nn in kq[kk]:
        vv = env[nn]
        vary_kq[kk].append(xt.Vary(nn, step=1e-6, tag=kk)) # Note the small step
vary_all = []
for kk in kq.keys():
    vary_all += vary_kq[kk]

tar_bet = [
   xt.TargetSet(at='qfs1a::0', betx=xt.LessThan(140.)),
   xt.TargetSet(at='qfs3a::0', betx=xt.LessThan(140), bety=xt.GreaterThan(25.)),
   xt.TargetSet(at='qfs5a::0', betx=xt.LessThan(190), bety=xt.GreaterThan(25.)),
   xt.TargetSet(at='qfl2a::0', betx=xt.LessThan(260)),
   xt.TargetSet(at='qfl3a::0', betx=xt.LessThan(env['bxmax']), bety=xt.GreaterThan(62)),
   xt.TargetSet(at='qfl6a::0', betx=xt.LessThan(env['bxmax'])),
   xt.TargetSet(at='qfl4a::0', betx=xt.LessThan(env['bxmax']), bety=xt.GreaterThan(65)),
   xt.TargetSet(at='qfl5a::0', betx=xt.LessThan(env['bxmax'])),
   xt.TargetSet(at='qds0a::0', bety=xt.LessThan(155)),
   xt.TargetSet(at='qds2a::0', bety=xt.LessThan(155)),
   xt.TargetSet(at='qds4a::0', bety=xt.LessThan(155)),
   xt.TargetSet(at='qdl1a::0', bety=xt.LessThan(235)),
   xt.TargetSet(at='qdl2a::0', bety=xt.LessThan(env['bymax'])),
   xt.TargetSet(at='qdl3a::0', bety=xt.LessThan(env['bymax'])),
   xt.TargetSet(at='qdl4a::0', bety=xt.LessThan(env['bymax'])),
   xt.TargetSet(at='qdl5a::0', bety=xt.LessThan(env['bymax'])),
   xt.TargetSet(at='qdl5a::2', bety=xt.LessThan(env['bymax']))
]
tar_center = xt.TargetSet(at='scenter::0', betx=env['bxsc'], bety=env['bysc'],
                          alfx=0, alfy=0,
                          dx=0, dpx=0)

tar_end = xt.TargetSet(at=xt.END,
    betx=tw_uu.betx[0], bety=tw_uu.bety[0], alfx=0, alfy=0,
    dx=tw_uu.dx[0], dpx=tw_uu.dpx[0],
    mux = tw_uu.mux[-1] * 0.5 + 3.0,
    muy = tw_uu.muy[-1] * 0.5 + 3.0)

opt_full = line.match(
    solve=False,
    method='4d',
    vary=vary_kq['ussu'],
    betx=tw_uu.betx[0], bety=tw_uu.bety[0],
    alfx=tw_uu.alfx[0], alfy=tw_uu.alfy[0],
    dx=tw_uu.dx[0], dpx=tw_uu.dpx[0],
    targets=tar_bet + [tar_center, tar_end],
)

# Initialize quads with a small strength
for vv in vary_all:
    nn = vv.name
    if env.vars.vary_default[nn]['limits'][1] > 1e-3:
        env[nn] = 1e-3
    else:
        env[nn] = -1e-3

opt_ss = opt_full.clone(
    add_targets=[
        xt.TargetSet(at='qdl1a::0', dx=0, dpx=0, weight=10000),
        xt.TargetSet(at='qfl2a::0', dx=0, dpx=0, weight=10000),
        xt.TargetSet(at='qdl2a::0', betx=xt.GreaterThan(50)),
        xt.TargetSet(at='qfl6a::0', bety=xt.GreaterThan(70)),
        xt.TargetSet(at='qdl4a::0', betx=xt.GreaterThan(80)),
    ]
    )
opt = opt_ss

opt.step(20)
opt._step_simplex(1000)
opt.step(20)
opt._step_simplex(1000)
opt.step(50)
opt._step_simplex(1000)
opt.step(50)
opt._step_simplex(10000)

opt.targets['END_mux'].weight = 1000
opt.targets['END_muy'].weight = 1000
opt.step(50)
opt._step_simplex(1000)
opt.step(50)
opt._step_simplex(1000)
opt.step(50)
opt._step_simplex(10000)

opt_full.tag('final')

import json
with open('strengths_quads_06_straight.json', 'w') as fid:
    json.dump(opt_full.get_knob_values(-1), fid, indent=1)