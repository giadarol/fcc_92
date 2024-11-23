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

ks = {}
ks['cell'] = ['ksffam1', 'ksffam2', 'ksdfam1', 'ksdfam2']

# Build vary objects keeping the initial signs
vary_kq = {}
for kk in kq.keys():
    vary_kq[kk] = []
    for nn in kq[kk]:
        vary_kq[kk].append(xt.Vary(nn, step=1e-6, tag=kk))

vary_ks = {}
for kk in ks.keys():
    vary_ks[kk] = []
    for nn in ks[kk]:
        vary_ks[kk].append(xt.Vary(nn, step=1e-4, tag=kk))
vary_all = []
for kk in kq.keys():
    vary_all += vary_kq[kk]
for kk in kq.keys():
    vary_all += vary_ks[kk]

tar_mu = xt.TargetSet(at=xt.END, mux=env['muxu'], muy=env['muyu'])
tar_dx = xt.Target(lambda tw: tw.rows['qf.*']['dx'].std(), xt.LessThan(0.001), tag='dx', weight=1000)
tar_betx = xt.Target(lambda tw: tw.rows['qf.*']['betx'].std(), xt.LessThan(0.1), tag='betx')
tar_bety = xt.Target(lambda tw: tw.rows[['qd3a::0', 'qd5a::0', 'qd5a::1', 'qd3a::1','qd1a::1']]['bety'].std(), 
                     xt.LessThan(0.1), tag='bety')
tar_chrom = xt.TargetSet(dqx=env['dqx_cell'], dqy=env['dqy_cell'])

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

# Put a small strength on quadrupoles and sextupoles
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
opt._step_simplex(100)
opt.step(20)
opt._step_simplex(100, xatol=1e-8, fatol=1e-10)
opt.disable(target='bet.*')
opt.step(20)

import json
with open('strengths_quads_00_arc_cell.json', 'w') as fid:
    json.dump(opt_quads.get_knob_values(-1), fid)

# Match chromaticity
opt_chrom = line.match(
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
    solve=False,
    method='4d',
    vary=vary_kq['cell'],
    targets=xt.TargetSet(qx=254.2, qy=222.2)
)
opt = opt_tune_star
opt.step(20)
tw_sf = line_starfish.twiss4d(strengths=True)

nemitt_x=1e-7
nemitt_y=1e-8

n_test = 20
p_test_x = line_starfish.build_particles(
    method='4d',
    x_norm=np.linspace(0, 400, n_test),
    y_norm=0,
    nemitt_x=nemitt_x,
    nemitt_y=nemitt_y,
)

p_test_y = line_starfish.build_particles(
    method='4d',
    x_norm=0,
    y_norm=np.linspace(0, 400, n_test),
    nemitt_x=nemitt_x,
    nemitt_y=nemitt_y,
)

p_test_xy = line_starfish.build_particles(
    method='4d',
    x_norm=np.linspace(0, 400, n_test),
    y_norm=np.linspace(0, 400, n_test),
    nemitt_x=nemitt_x,
    nemitt_y=nemitt_y,
)

def starfish(plot=False):
    line_starfish.track(num_turns=6, particles=p_test_x.copy(), turn_by_turn_monitor=True)
    mon_x = line_starfish.record_last_track
    ncoord_x = tw_sf.get_normalized_coordinates(mon_x,
                                            nemitt_x=nemitt_x, nemitt_y=nemitt_y)


    line_starfish.track(num_turns=6, particles=p_test_y.copy(), turn_by_turn_monitor=True)
    mon_y = line_starfish.record_last_track
    ncoord_y = tw_sf.get_normalized_coordinates(mon_y,
                                            nemitt_x=nemitt_x, nemitt_y=nemitt_y)

    line_starfish.track(num_turns=6, particles=p_test_xy.copy(), turn_by_turn_monitor=True)
    mon_xy = line_starfish.record_last_track
    ncoord_xy = tw_sf.get_normalized_coordinates(mon_xy,
                                            nemitt_x=nemitt_x, nemitt_y=nemitt_y)

    if plot:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(6.4*2.2, 4.8))
        plt.subplot(131)
        plt.plot(ncoord_x.x_norm, ncoord_x.px_norm, '.')
        plt.axis('equal')
        plt.xlabel('x')
        plt.ylabel('px')
        plt.subplot(132)
        plt.plot(ncoord_y.y_norm, ncoord_y.py_norm, '.')
        plt.axis('equal')
        plt.xlabel('y')
        plt.ylabel('py')
        plt.subplot(133)
        plt.plot(ncoord_xy.x_norm, ncoord_xy.py_norm, '.')
        plt.axis('equal')
        plt.xlabel('x=y')
        plt.ylabel('py')

    out ={'ncoord_x': ncoord_x._data, 'ncoord_y': ncoord_y._data, 'ncoord_xy': ncoord_xy._data}

    px_norm_rms_5 = ncoord_x.px_norm[:, 5].std()
    pxy_norm_rms_5 = ncoord_xy.py_norm[:, 5].std()
    out['px_norm_rms_5'] = px_norm_rms_5
    out['pxy_norm_rms_5'] = pxy_norm_rms_5

    return out

class ActionStarfish(xt.Action):

    def run(self):
        return starfish()

act = ActionStarfish()
opt_starfish = line.match(
    solve=False,
    method='4d',
    vary=vary_ks['cell'],
    targets=[tar_chrom,
             act.target('px_norm_rms_5', 0),
             act.target('pxy_norm_rms_5', 0)]
)
opt = opt_starfish
opt.step(10)

out = {}
sext_strengths = ['ksf1', 'ksf2', 'ksf3', 'ksf4',
                  'ksd1', 'ksd2', 'ksd3', 'ksd4']
out.update(env.vars.get_table().rows[sext_strengths].to_dict())
out.update(opt_starfish.get_knob_values(-1))

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
