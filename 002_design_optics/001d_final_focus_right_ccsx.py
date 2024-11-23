import numpy as np
import xtrack as xt
import time

env = xt.Environment()
env.call('../fccee_z_lattice.py')
env.call('quad_strength_limits.py')

env.vars.load_json('strengths_quads_03_ffccsyr.json')

env.call('matching_constraints.py')

line = -env['ccs_yr'] + (-env['ccs_xr'])

tt0 = line.get_table(attr=True)
tt0_quad = tt0.rows[tt0.element_type == 'Quadrupole']
tt0_sext = tt0.rows[tt0.element_type == 'Sextupole']

kq = {}
kq['section_c'] = ['kqd07r', 'kqf08r', 'kqd09r', 'kqf10r']
kq['section_d'] = ['kqd11r', 'kqf12r']
kq['xquads'] = ['kqx00r', 'kqx01r', 'kqx02r']
kq['section_e'] = ['kqf13r', 'kqd14r', 'kqf15r', 'kqd16r',
                   'kqf17r', 'kqd18r', 'kqf19r', 'kqd20r']

# Build vary objects keeping the initial signs
vary_kq = {}
for kk in kq.keys():
    vary_kq[kk] = []
    for nn in kq[kk]:
        vv = env[nn]
        vary_kq[kk].append(xt.Vary(nn, step=1e-10, tag=kk)) # Note the small step
vary_all = []
for kk in kq.keys():
    vary_all += vary_kq[kk]

tar_sfm2r = xt.TargetSet(betx=xt.LessThan(60.0),
                     bety=xt.LessThan(20.0),
                     alfx=xt.GreaterThan(0.),
                     dx=xt.GreaterThan(env['dx_sfmr']),
                     at='sfm2r::0')

tar_sfx1r= xt.TargetSet(
                     betx=xt.LessThan(965),
                     alfx=0,
                     bety=xt.LessThan(50.),
                     dx=xt.LessThan(1.),
                     mux=1.75 - 0.007,
                     at='sfx1r::1')

tar_rmat_sext = xt.TargetRmatrix(start='sfx1r::1', end='sfx2r::1',
                        r12=env['r12_ccsxl'], r34=env['r34_ccsxl'],
                        r11=-1, r33=-1)

tar_imag4 = xt.TargetSet(betx=xt.GreaterThan(0.5), bety=xt.LessThan(35.),
                         alfx=0, alfy=0.18,
                         dx=xt.GreaterThan(0.001),
                         dpx=env['dpx_ccxr'],
                         at='ipimag4')

tar_rmat_end = xt.TargetRmatrix(start=xt.START, end=xt.END,
                                r33=0, r12=0)

tar_end = xt.TargetSet(betx=env['bx_ff_out'], alfx=0.0,
                       bety=env['by_ff_out'], alfy=0.0,
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
for kk in ['ksdy1r', 'ksdy2r', 'ksdm1r', 'ksdm1r', 'ksfm2r',
           'ksfx1r', 'kcrabr']:
    env[kk] = 0.

# Match ipimag3
opt_sfm2r = line.match(
    name='imag3',
    solve=False,
    betx=env['bxip'],
    bety=env['byip'],
    targets=[tar_sfm2r,
             xt.TargetSet(dx=xt.LessThan(0.45), at='qf10r')],
    vary=vary_kq['section_c']
)
opt = opt_sfm2r
opt.step(100)

# March to sfx1
opt_sfx1r = opt_sfm2r.clone(name='sfx1r_d',
                              add_vary=vary_kq['section_d'],
                              add_targets=tar_sfx1r)
opt = opt_sfx1r
opt.step(100)

opt_more_sfx1r = opt_sfx1r.clone(name='sfx1r_cd',
                           add_vary=vary_kq['section_c'])
opt = opt_more_sfx1r
opt.step(100)


# Match r matrix alone
opt_rsext = line.match(
    name='rmat_sext',
    solve=False,
    start='sfx1r::1', end='sfx2r::1',
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
opt_imag4 = opt_more_sfx1r.clone(name='imag4',
                                 add_targets=tar_imag4)
opt = opt_imag4

# Focus on optics at sextupole
opt_imag4.disable(target=True)
opt_imag4.enable(target='sfx1r.*')
opt.step(200)
opt.enable(target=True)

# Add rmatrix and qy quads
opt_imag4_with_qy = opt_imag4.clone(
    name='imag4_with_qy',
    add_vary=vary_kq['xquads'],
    add_targets=tar_rmat_sext)
opt = opt_imag4_with_qy
opt.enable(True)
opt.step(100)

opt.targets['ipimag4_dpx'].weight = 1000
opt.step(100)

# Try to close with downstream quadrupoles alone
opt_end = opt_imag4_with_qy.clone(
    name='end',
    remove_vary=True,
    remove_targets=True,
    add_vary=vary_kq['section_e'],
    add_targets=[tar_end,
                 xt.TargetSet(dx=0, dpx=0, at='qf17r'), # to prevent dx going wild in the straight
    ]
)
opt = opt_end

opt.disable(target='END_mu.*')
opt.step(100)
opt.enable(target='END_mu.*')
opt.step(100)

opt.targets[5].weight = 1000
opt.step(100)

opt.plot()

# Refine with symplex
opt_imag4_with_qy._step_simplex(1000)
opt_end._step_simplex(1000)

opt_full = opt_end.clone(
    name='full',
    add_targets=opt_imag4_with_qy.targets,
    add_vary=opt_imag4_with_qy.vary
)
opt = opt_full
opt.step(200)

opt_full._step_simplex(1000)

import json
with open('strengths_quads_04_ffccsxr.json', 'w') as fid:
    json.dump(opt_full.get_knob_values(-1), fid, indent=1)