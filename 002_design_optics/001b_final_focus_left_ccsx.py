import numpy as np
import xtrack as xt
import time

env = xt.Environment()
env.call('../fccee_z_lattice.py')
env.call('quad_strength_limits.py')

env.vars.load_json('strengths_quads_01_ffccsyl.json')

env.call('matching_constraints.py')

line = -env['ccs_yl'] + (-env['ccs_xl'])

tt0 = line.get_table(attr=True)
tt0_quad = tt0.rows[tt0.element_type == 'Quadrupole']
tt0_sext = tt0.rows[tt0.element_type == 'Sextupole']

kq = {}
kq['section_c'] = ['kqd07l', 'kqf08l', 'kqd09l', 'kqf10l']
kq['section_d'] = ['kqd11l', 'kqf12l']
kq['xquads'] = ['kqx00l', 'kqx01l', 'kqx02l']
kq['section_e'] = ['kqf13l', 'kqd14l', 'kqf15l', 'kqd16l',
                   'kqf17l', 'kqd18l', 'kqf19l', 'kqd20l']

# Build vary objects keeping the initial signs
vary_kq = {}
for kk in kq.keys():
    vary_kq[kk] = []
    for nn in kq[kk]:
        vv = env[nn]
        vary_kq[kk].append(xt.Vary(nn, step=1e-10, tag=nn))
vary_all = []
for kk in kq.keys():
    vary_all += vary_kq[kk]

tar_sfm2l = [
        xt.TargetSet(betx=xt.LessThan(27.0),
                     bety=xt.LessThan(15.0),
                     alfx=xt.GreaterThan(0.),
                     alfy=xt.GreaterThan(0.5),
                     dx=xt.GreaterThan(0.235),
                     at='sfm2l::0'),
        xt.TargetSet(alfy=xt.LessThan(0.9), dx=xt.LessThan(0.25),
                     at='sfm2l::0')]

tar_sfx1l= xt.TargetSet(betx=xt.GreaterThan(1000.),
                     alfx=0,
                     bety=xt.LessThan(45.),
                     dx=xt.LessThan(0.6),
                     mux=1.75 - 0.0093,
                     at='sfx1l::1')

tar_rmat_sext = xt.TargetRmatrix(start='sfx1l::1', end='sfx2l::1',
                        r12=env['r12_ccsxl'], r34=env['r34_ccsxl'],
                        r11=-1, r33=-1)

tar_imag4 = xt.TargetSet(betx=xt.LessThan(20), bety=xt.LessThan(25.),
                         alfx=0, alfy=env['delta_alfy_ccsx'],
                         dx=xt.GreaterThan(2e-3),
                         dpx=env['dpx_ccxl'],
                         at='ipimag4')

tar_rmat_end = xt.TargetRmatrix(start=xt.START, end=xt.END,
                                r33=0, r12=0)

tar_end = xt.TargetSet(betx=env['bx_ff_out'], alfx=0.0,
                       bety=env['by_ff_out'], alfy = 0.0,
                       dx=env['dx_ff_out'], dpx=0.0,
                       mux=3.0, muy=2.75, at=xt.END)


# Initialize quads with a small strength
for vv in vary_all:
    nn = vv.name
    if env.vars.vary_default[nn]['limits'][1] > 1e-3:
        env[nn] = 1e-3
    else:
        env[nn] = -1e-3

# wipe sextupoles
for kk in ['ksdy1l', 'ksdy2l', 'ksdm1l', 'ksdm1l', 'ksfm2l',
           'ksfx1l', 'kcrabl']:
    env[kk] = 0.

# Match ipimag3
opt_ipimag3 = line.match(
    name='imag3',
    solve=False,
    betx=env['bxip'],
    bety=env['byip'],
    targets=tar_sfm2l + [
        # xt.TargetSet(bety=xt.LessThan(780), betx=xt.LessThan(140), at='qd9l')
        ],
    vary=vary_kq['section_c'])
opt = opt_ipimag3
opt.disable(target=True)
opt.enable(target=['sfm2l::0_betx', 'sfm2l::0_bety', 'sfm2l::0_dx'])
opt.step(200)
opt.enable(target=True)
opt.step(200)

# March to sfx1
opt_sfx1l = opt_ipimag3.clone(name='sfx1l_d',
                              remove_vary=True,
                              add_vary=vary_kq['section_d'],
                              add_targets=tar_sfx1l)
opt = opt_sfx1l
opt.step(100)

opt_more_sfx1l = opt_sfx1l.clone(name='sfx1l_cd',
                           add_vary=vary_kq['section_c'])
opt = opt_more_sfx1l
opt.step(100)

# Match r matrix alone
opt_rsext = line.match(
    name='rmat_sext',
    solve=False,
    start='sfx1l::1', end='sfx2l::1',
    init_at='ipimag4',
    betx=0.20, bety=0.20, # Rough estimate
    targets=tar_rmat_sext,
    vary=vary_kq['xquads'])

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

# Imag 4 without r matrix
opt_imag4 = opt_more_sfx1l.clone(name='imag4',
                                 add_targets=tar_imag4)
opt = opt_imag4
opt.step(200)

# Focus on optics at sextupole
opt.disable(target=True)
opt.enable(target='sfx1l.*')
opt.step(200)


# Add rmatrix and qy quads
opt_imag4_with_qy = opt_imag4.clone(
    name='imag4_with_qy',
    add_vary=vary_kq['xquads'],
    add_targets=tar_rmat_sext)
opt = opt_imag4_with_qy
opt.enable(True)
opt.step(100)

opt.disable(target=True)
opt.enable(target='ipimag4_.*')
opt.step(100)

opt.enable(target=True)
opt.targets['ipimag4_dx'].weight = 10000
opt.targets['ipimag4_dpx'].weight = 10000
opt.step(100)

opt.targets['sfx1l::1_mux'].weight = 1000
opt.step(100)

# Try to close with downstream quadrupoles alone
opt_end = opt_imag4_with_qy.clone(
    name='end',
    remove_vary=True,
    remove_targets=True,
    add_vary=vary_kq['section_e'],
    add_targets=[tar_end,
                 xt.TargetSet(dx=0, dpx=0, at='qf17l'), # to prevent dx going wild in the straight
                 xt.TargetSet(bety=xt.LessThan(2000), at='qf17l'),
                 xt.TargetSet(bety=xt.LessThan(2000), at='qd18l'),
                 xt.TargetSet(bety=xt.LessThan(2000), at='qf19l'),
                 xt.TargetSet(bety=xt.LessThan(2000), at='qd20l'),
                 xt.TargetSet(bety=xt.GreaterThan(750), at='qf19l'),
    ]
)
opt = opt_end

opt.targets['END_dx'].weight = 100
opt.targets['END_dpx'].weight = 100

opt.step(5)
opt._step_simplex(10000)

# from scipy.optimize import least_squares
# fff = opt.get_merit_function()
# bounds=fff.get_x_limits()
# res = least_squares(fff, fff.get_x(), bounds=(bounds[:, 0], bounds[:, 1]),
#                                               method='trf', verbose=1, ftol=1e-14, xtol=1e-14, gtol=1e-14)

opt_full = opt_end.clone(
    name='full',
    add_targets=opt_imag4_with_qy.targets,
    add_vary=opt_imag4_with_qy.vary
)
opt = opt_full
opt.step(200)

opt_full._step_simplex(1000)

opt.plot()
opt_full.target_mismatch(ret=True).show()

tt = line.get_table(attr=True)
tt_quad = tt.rows[tt.element_type == 'Quadrupole']

opt_full.tag('final')

import json
with open('strengths_quads_02_ffccsxl.json', 'w') as fid:
    json.dump(opt_full.get_knob_values(-1), fid, indent=1)