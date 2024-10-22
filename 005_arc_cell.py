import xtrack as xt
import numpy as np

env = xt.Environment()
env.call('fccee_z_parameters.py')
env.call('fccee_z_elements.py')
env.call('fccee_z_lattice.py')
env.call('fccee_z_strengths.py')

line = env['cell_u']
tw0 = line.twiss4d(strengths=True)

tt0 = line.get_table(attr=True)
tt0_quad = tt0.rows[tt0.element_type == 'Quadrupole']
tt0_sext = tt0.rows[tt0.element_type == 'Sextupole']


kq = {}
kq['cell'] = ['kqd1', 'kqf2', 'kqd3', 'kqf4', 'kqd5', 'kqf6']

ks = {}
ks['cell'] = ['ksffam1', 'ksffam2', 'ksdfam1', 'ksdfam2']

# Build vary objects keeping the initial signs
vary_kq = {}
for kk in kq.keys():
    vary_kq[kk] = []
    for nn in kq[kk]:
        vv = env[nn]
        vary_kq[kk].append(xt.Vary(nn, step=1e-6,
                    limits={False:(-10, 0.), True:(0., 10.)}[vv>=0.], tag=kk))

vary_ks = {}
for kk in ks.keys():
    vary_ks[kk] = []
    for nn in ks[kk]:
        vv = env[nn]
        vary_ks[kk].append(xt.Vary(nn, step=1e-4,
                    limits={False:(-10, 0.), True:(0., 10.)}[vv>=0.], tag=kk))
vary_all = []
for kk in kq.keys():
    vary_all += vary_kq[kk]
for kk in kq.keys():
    vary_all += vary_ks[kk]

tar_mu = xt.TargetSet(at=xt.END,mux=env['muxu'], muy=env['muyu'])
tar_bet = xt.Target(lambda tw: tw.rows['qf.*']['betx'].std(), 0., tag='betx')
tar_chrom = xt.TargetSet(dqx=tw0.dqx, dqy=tw0.dqy)

opt_pant = line.match(
    solve=False,
    method='4d',
    targets=[tar_mu, tar_bet, tar_chrom],
    vary=vary_all,
)
opt = opt_pant

line_starfish = 3*120 * env['cell_u']

# Put the fractional tune on 0.2
opt_tune_star = line_starfish.match(
    solve=False,
    method='4d',
    vary=vary_kq['cell'],
    targets=xt.TargetSet(qx=254.2, qy=222.2)
)
opt = opt_tune_star
opt.step(20)
tw_sf = line_starfish.twiss4d(strengths=True)

nemitt_x=1e-7
nemitt_y=1e-7

n_test = 50
p_test = line_starfish.build_particles(
    method='4d',
    x_norm=np.linspace(0, 200, n_test),
    y_norm=np.linspace(0, 200, n_test),
    nemitt_x=nemitt_x,
    nemitt_y=nemitt_y,
)

line_starfish.track(num_turns=6, particles=p_test, turn_by_turn_monitor=True,
           with_progress=1)
mon = line_starfish.record_last_track

ncoord = tw_sf.get_normalized_coordinates(mon,
                                          nemitt_x=nemitt_x, nemitt_y=nemitt_y)


import matplotlib.pyplot as plt
plt.close('all')
plt.figure(1)
plt.plot(ncoord.y_norm, ncoord.py_norm, '.')
plt.axis('equal')
plt.show()

prrrrr

# wipe all quads and sextupoles
for kk in opt_pant.get_knob_values(0).keys():
    env[kk] = 0.01 * np.sign(env[kk])

opt_quads = line.match(
    solve=False,
    method='4d',
    vary=vary_kq['cell'],
    targets=[tar_mu, tar_bet]
)
opt = opt_quads
opt.step(10)
opt._step_simplex(1000)

# Match chromaticity
