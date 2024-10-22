import numpy as np
import xtrack as xt
import time

# Needs:
#  - access targets and vary by name
#  - automatic tag generation for targets
#  - add opt.twiss
#  - env.vars.update
#  - target/vary state should be a property of the optimizer

env = xt.Environment()
env.call('fccee_z_parameters.py')
env.call('fccee_z_elements.py')
env.call('fccee_z_lattice.py')
env.call('fccee_z_strengths.py')

line = env['mccs_yl']

tt0 = line.get_table(attr=True)
tt0_quad = tt0.rows[tt0.element_type == 'Quadrupole']
tt0_sext = tt0.rows[tt0.element_type == 'Sextupole']

tw0 = line.twiss(betx=env['bxip'], bety=env['byip'], strengths=True)

kq = {}
kq['triplet'] = ['kqd0al', 'kqd0bl', 'kqf1al']
kq['section_a'] = ['kqd01l', 'kqf02l', 'kqd02l']
kq['section_b'] = ['kqd04l', 'kqf05l', 'kqd06l']
kq['yquads'] = ['kqy01l', 'kqy02l', 'kqy03l', 'kqy04l']

# Build vary objects keeping the initial signs
vary_kq = {}
for kk in kq.keys():
    vary_kq[kk] = []
    for nn in kq[kk]:
        vv = env[nn]
        vary_kq[kk].append(xt.Vary(nn, step=1e-8, #!!!!
                    limits={False:(-10, 0.), True:(0., 10.)}[vv>=0.], tag=kk))
vary_all = []
for kk in kq.keys():
    vary_all += vary_kq[kk]

# Targets adapted based on what is found in the optics
tar_sdm1l = xt.TargetSet(betx=xt.LessThan(10.), bety=xt.LessThan(12.),
                     alfx=xt.GreaterThan(-1.), alfy=0.0,
                     at='sdm1l::0')
tar_sdy1l = xt.TargetSet(bety=8114.3, betx=371.7,
                     alfy=0., dx=xt.GreaterThan(0.3),
                     muy=0.75+env['dmuy_sdy1l'],
                     at='sdy1l::1')
tar_ipimag2 = xt.TargetSet(betx=xt.GreaterThan(60.), alfx=0., alfy=0.,
                     dx=0.302, dpx=0,
                     at='ipimag2')
tar_rmat_sext = xt.TargetRmatrix(start='sdy1l::1', end='sdy2l::1',
                r12=env['r12_ccsyl'], r34=env['r34_ccsyl'],
                r33=-1.0, r43=0.0, tol=1e-6, tag='rmat_sext')

opt_pant = line.match(
    solve=False,
    betx=env['bxip'],
    bety=env['byip'],
    targets=[tar_sdm1l , tar_sdy1l, tar_ipimag2, tar_rmat_sext],
    vary=vary_all,
    )

# wipe all quads
for kk in opt_pant.get_knob_values(0).keys():
    env[kk] = 0.001 * np.sign(env[kk])

# wipe sextupoles
for kk in ['ksdy1l', 'ksdy2l', 'ksdm1l', 'ksdm1l', 'ksfm2l',
           'ksfx1l', 'kclabl']:
    env[kk] = 0.

opt_triplet = line.match(
    name='triplet',
    solve=False,
    betx=env['bxip'],
    bety=env['byip'],
    targets=[
        xt.TargetSet(bety=xt.LessThan(8550), at='qd0bl'),

        xt.TargetSet(bety=xt.LessThan(3500), at='qf1bl'), # This quad is off!
        xt.TargetSet(bety=xt.GreaterThan(3300), at='qf1bl'),
        # End of final focus

        xt.TargetSet(betx=xt.GreaterThan(1300), at='qd1l'),
        xt.TargetSet(betx=xt.LessThan(1400), at='qd1l'),
        xt.TargetSet(bety=xt.LessThan(3200), at='qd1l'),
        xt.TargetSet(bety=xt.GreaterThan(3100), at='qd1l'),
    ],
    vary = vary_kq['triplet']
)
opt = opt_triplet
opt.step(100)

opt_sdm1l = opt_triplet.clone(
    name='sdm1l', remove_vary=True,
    add_targets=[tar_sdm1l] + [
        xt.TargetSet(betx=xt.LessThan(3000), at='qf2l'),
        xt.TargetSet(bety=xt.GreaterThan(900), at='qf2l'),
    ],  add_vary=vary_kq['section_a'])
opt = opt_sdm1l
opt.step(100)

opt_dsdy1l = opt_sdm1l.clone(
    name='sdy1l', remove_targets=True, remove_vary=True,
    add_targets=[tar_sdy1l], add_vary=vary_kq['section_b'])
opt = opt_dsdy1l
opt.step(100)

# Refine optics at first sextupole using sections a and b (no other target)
opt_dsdy1l_refine = opt_dsdy1l.clone(name='dsdy1l_refine',
                                     add_vary=vary_kq['section_a'])
opt = opt_dsdy1l_refine
opt.step(100)

# Match r matrix s1/s2
opt_rsext = line.match(
    name='rmat_sext',
    solve=False,
    start='sdy1l::1', end='sdy2l::1', init_at='ipimag2',
    betx=135, bety=10, # Rough estimate
    targets=tar_rmat_sext, vary=vary_kq['yquads'])
opt = opt_rsext
opt.disable(target=True)
opt.enable(target=0)
opt.step(20)
opt.enable(target=1)
opt.step(20)
opt.enable(target=2)
opt.step(20)
opt.enable(target=3)
opt.step(20)


opt_imag2_with_qy = opt_dsdy1l.clone(
    name='imag2_with_qy',
    add_vary=vary_kq['section_a'] + vary_kq['yquads'],
    add_targets=[tar_ipimag2, tar_sdm1l, tar_rmat_sext])
opt = opt_imag2_with_qy
opt.step(100)


# Refine rmatrix
opt.disable(target=True, vary=True)
opt.enable(target='rmat_sext', vary='yquads')
opt.step(100)
opt.enable(target=True, vary=True)

# Refine the phase at sdy1r
opt.disable(target=True, vary=True)
opt.enable(target='sdy1r.*', vary=['section_b'])
opt.step(100)
opt.enable(target=True, vary=True)

# Full optimizer
opt_full = opt_imag2_with_qy.clone(name='full',
                        add_targets=opt_triplet.targets,
                        add_vary=opt_triplet.vary)
opt = opt_full
opt.enable(target=True, vary=True)
opt.targets[3].weight = 1000
opt.targets[9].weight = 1000
opt.step(100)

# To get the fine digits
opt._step_simplex(10000)

opt.plot()

opt_pant.tag('gianni')
import json
with open('mccs_yl.json', 'w') as fid:
    json.dump(opt_pant.get_knob_values(-1), fid)

