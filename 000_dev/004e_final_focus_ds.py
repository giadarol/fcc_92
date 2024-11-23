import numpy as np
import xtrack as xt

# Needs:
#  - access targets and vary by name
#  - automatic tag generation for targets
#  - add opt.twiss
#  - env.vars.update

env = xt.Environment()
env.call('fccee_z_parameters.py')
env.call('fccee_z_elements.py')
env.call('fccee_z_lattice.py')
env.call('fccee_z_strengths.py')

# Load cell strengths from my match
env.vars.load_json('strengths_quads_00_arc_cell.json')

line = env['cell_uffl']

tt0 = line.get_table(attr=True)
tt0_quad = tt0.rows[tt0.element_type == 'Quadrupole']
tt0_sext = tt0.rows[tt0.element_type == 'Sextupole']

tw_uu = env['arc_uu'].twiss4d()

kq = {}
kq['uffl'] = [
    'kqfm0l', 'kqdm0l', 'kqfm1l', 'kqdm2l', 'kqfm3l',
    'kqdm4l', 'kqfm5l', 'kqdm6l', 'kqfm7l', 'kqdm8l',
]
# Build vary objects keeping the initial signs
vary_kq = {}
for kk in kq.keys():
    vary_kq[kk] = []
    for nn in kq[kk]:
        vv = env[nn]
        vary_kq[kk].append(xt.Vary(nn, step=1e-6,
                    limits={False:(-10, 0.), True:(0., 10.)}[vv>=0.], tag=kk))

tw0 = line.twiss(
    betx=tw_uu.betx[0], bety=tw_uu.bety[0],
    alfx=tw_uu.alfx[0], alfy=tw_uu.alfy[0],
    dx=tw_uu.dx[0], dpx=tw_uu.dpx[0])

opt_pant = line.match(
    solve=False,
    method='4d',
    vary=vary_kq['uffl'],
    betx=tw_uu.betx[0], bety=tw_uu.bety[0],
    alfx=tw_uu.alfx[0], alfy=tw_uu.alfy[0],
    dx=tw_uu.dx[0], dpx=tw_uu.dpx[0],
    targets=[
        xt.TargetSet(at=xt.END,
            betx=env['bx_ff_out'],
            bety=env['by_ff_out'],
            alfx=0, alfy=0, dx=0, dpx=0,
            mux = tw_uu.mux[-1]  * 0.25 + 0.50,
            muy = tw_uu.muy[-1]  * 0.25 + 0.50),
        xt.TargetSet(dx=0, dpx=0, at='qdm6l', weight=1000),
        xt.TargetSet(dx=0, dpx=0, at='qfm5l', weight=1000),
        xt.TargetSet(bety=xt.GreaterThan(350), at='qfm5l'),
        xt.TargetSet(bety=xt.GreaterThan(600), at='qfm7l'),
        xt.TargetSet(bety=xt.LessThan(600), at='qdm6l'),
        xt.TargetSet(betx=xt.LessThan(200), bety=xt.LessThan(200), at='qfm0l'),
        xt.TargetSet(betx=xt.LessThan(200), bety=xt.LessThan(200), at='qfm1l'),
        xt.TargetSet(betx=xt.LessThan(200), bety=xt.LessThan(200), at='qdm2l'),
        xt.TargetSet(betx=xt.LessThan(200), bety=xt.LessThan(200), at='qfm3l'),
        xt.TargetSet(betx=xt.LessThan(200), bety=xt.LessThan(200), at='qdm4l'),
    ],
)

# wipe all quads
for kk in opt_pant.get_knob_values(0).keys():
    env[kk] = 0.001 * np.sign(env[kk])

opt_end = opt_pant.clone()
opt = opt_end
opt.step(50)
opt._step_simplex(1000)
opt.step(50)
opt._step_simplex(1000)

# Other side is symmetric

kq_right = ['kqfm0r', 'kqdm0r', 'kqfm1r', 'kqdm2r', 'kqfm3r',
            'kqdm4r', 'kqfm5r', 'kqdm6r', 'kqfm7r', 'kqdm8r']

env['kqfm0r'] = 'kqfm0l'
env['kqdm0r'] = 'kqdm0l'
env['kqfm1r'] = 'kqfm1l'
env['kqdm2r'] = 'kqdm2l'
env['kqfm3r'] = 'kqfm3l'
env['kqdm4r'] = 'kqdm4l'
env['kqfm5r'] = 'kqfm5l'
env['kqdm6r'] = 'kqdm6l'
env['kqfm7r'] = 'kqfm7l'
env['kqdm8r'] = 'kqdm8l'

tt_kqright = line.vars.get_table().rows[kq_right]

opt_pant.tag('gianni')

import json
out = {}
out.update(opt_pant.get_knob_values())
out.update(tt_kqright.to_dict())

with open('strengths_quads_05_ffds_lr.json', 'w') as fid:
    json.dump(out, fid, indent=1)

import matplotlib.pyplot as plt
plt.close('all')
opt.plot()
