import xtrack as xt
import numpy as np

from twiss_open_off_momentum import twiss_off_momentum, ActionOffMom

# Pantaleo's machine
env0 = xt.Environment()
env0.particle_ref = xt.Particles(mass0=xt.ELECTRON_MASS_EV, energy0=45.6e9)
env0.call('fccee_z_parameters.py')
env0.call('fccee_z_elements.py')
env0.call('fccee_z_lattice.py')
env0.call('fccee_z_strengths.py')
line = env0['fccee_p_ring']
line0 = line.copy()
section0 = line.select('mid_cell_edge_r::1','mid_cell_edge_l::2')
tw0_om = twiss_off_momentum(section=section0)
tw0_om_full = twiss_off_momentum(section=section0, delta_range=(-2e-2, 2e-2), num_delta=41,
                                 edge_l=0,edge_r=-1)
# env = env0

# Gianni's machine
env = xt.Environment()
env.particle_ref = xt.Particles(mass0=xt.ELECTRON_MASS_EV, energy0=45.6e9)
env.call('fccee_z_parameters.py')
env.call('fccee_z_elements.py')
env.call('fccee_z_lattice.py')
env.call('fccee_z_strengths.py')
env.vars.load_json('strengths_quads_00_arc_cell.json')
env.vars.load_json('strengths_quads_01_ffccsyl.json')
env.vars.load_json('strengths_quads_02_ffccsxl.json')
env.vars.load_json('strengths_quads_03_ffccsyr.json')
env.vars.load_json('strengths_quads_04_ffccsxr.json')
env.vars.load_json('strengths_quads_05_ffds_lr.json')
env.vars.load_json('strengths_quads_06_straight.json')
env.vars.load_json('strengths_sext_00_arc_cell.json')
env.vars.load_json('strengths_sext_01_straight.json')
line = env['fccee_p_ring']

section = line.select('mid_cell_edge_r::1','mid_cell_edge_l::2')
cell1 = line.select('mid_cell_edge_l::1','mid_cell_edge_r::1')
cell2 = line.select('mid_cell_edge_l::2','mid_cell_edge_r::2')

# section.replace_all_repeated_elements()
# section.cut_at_s(np.arange(0, section.get_length(), 0.3))

tw_cell_1 = cell1.twiss4d()
twinit_cell_1_r = tw_cell_1.get_twiss_init('mid_cell_edge_r')
tw_cell_2 = cell2.twiss4d()
twinit_cell_2_l = tw_cell_1.get_twiss_init('mid_cell_edge_l')

tt0 = section.get_table(attr=True)
tt0_quad = tt0.rows[tt0.element_type == 'Quadrupole']
tt0_sext = tt0.rows[tt0.element_type == 'Sextupole']

tt_mult_before = env.vars.get_table().rows['koct.*|kdec.*']

for kk in tt_mult_before.name:
    env[kk] = 0.

act = ActionOffMom(section=section)

tar_w_left = xt.TargetSet(wx_chrom=0, wy_chrom=0, at='ip_mid')
tar_w_right = xt.TargetSet(wx_chrom=0, wy_chrom=0, at='ip_mid')
tar_chrom3_left = [
    act.target('d3mux_l', 0, tol=0.1),
    act.target('d3muy_l', 0, tol=0.1),
]
tar_chrom3_right = [
    act.target('d3mux_r', 0, tol=0.1),
    act.target('d3muy_r', 0, tol=0.1),
]
tar_ddx_left = xt.TargetSet(ddx=0, ddpx=0, at='ip_mid')
tar_ddx_right = xt.TargetSet(ddx=0, ddpx=0, at='ip_mid')

opt_pant_left = section.match(
    name='pant_left',
    solve=False,
    init=twinit_cell_1_r,
    compute_chromatic_properties=True,
    vary=xt.VaryList(['ksfx1l', 'ksdy1l', 'ksdm1l', 'ksfm2l'], step=1e-3),
    targets=tar_w_left
)

opt_pant_right = section.match(
    name='pant_right',
    solve=False,
    init=twinit_cell_2_l,
    compute_chromatic_properties=True,
    vary=xt.VaryList(['ksfx1r', 'ksdy1r', 'ksdm1r', 'ksfm2r'], step=1e-3),
    targets=tar_w_right
)


# wipe ff sextupoles
for kk in ['ksfx1l', 'ksdy1l', 'ksdm1l', 'ksfm2l',
           'ksfx1r', 'ksdy1r', 'ksdm1r', 'ksfm2r',
           ]:
    env[kk] = 0.001 * np.sign(env[kk])

# Inspect sextupoles in special arc cells
sl_match = [
    'sf2al3', 'sd1al3', 'sf1al3', 'sd2al3',
    'sd2bl3', 'sf1bl3', 'sd1bl3', 'sf2bl3',
    'sf2afl', 'sd1afl', 'sf1afl', 'sd2afl',
    'sf3afl',
    'sf3afr', 'sd2afr', 'sf1afr', 'sd1afr',
    'sf2afr', 'sf2br3', 'sd1br3', 'sf1br3',
    'sd2br3', 'sd2ar3', 'sf1ar3', 'sd1ar3',
    'sf2ar3']

for ss in sl_match:
    ee = env[ss].get_expr('k2')
    print(ss, ee, ee._expr)

# # Define circuits in special cells
env.vars.default_to_zero = True
env['ksf2al3'] = 'ksffam2 + ksf2al3_delta'
env['ksd1al3'] = 'ksdfam1'
env['ksf1al3'] = 'ksffam1 + ksf1al3_delta'
env['ksd2al3'] = 'ksdfam2'
env['ksd2bl3'] = 'ksdfam2'
env['ksf1bl3'] = 'ksffam1 + ksf1bl3_delta'
env['ksd1bl3'] = 'ksdfam1'
env['ksf2bl3'] = 'ksffam2 + ksf2bl3_delta'
env['ksf2fl']  = 'ksffam2 + ksf2fl_delta'
env['ksd1fl']  = 'ksdfam1'
env['ksf1fl']  = 'ksffam1 + ksf1fl_delta'
env['ksd2fl']  = 0
env['ksf3fl']  = 0
env['ksf3fr']  = 0
env['ksd2fr']  = 0
env['ksf1fr']  = 'ksffam1 + ksf1fr_delta'
env['ksd1fr']  = 'ksdfam1'
env['ksf2fr']  = 'ksffam2 + ksf2fr_delta'
env['ksf2br3'] = 'ksffam2 + ksf2br3_delta'
env['ksd1br3'] = 'ksdfam1'
env['ksf1br3'] = 'ksffam1 + ksf1br3_delta'
env['ksd2br3'] = 'ksdfam2'
env['ksd2ar3'] = 'ksdfam2'
env['ksf1ar3'] = 'ksffam1 + ksf1ar3_delta'
env['ksd1ar3'] = 'ksdfam1'
env['ksf2ar3'] = 'ksffam2 + ksf2ar3_delta'
env.vars.default_to_zero = True

ddx_left_knobs = ['ksf2al3_delta', 'ksf1al3_delta', 'ksf1bl3_delta',
                  'ksf2bl3_delta', 'ksf2fl_delta', 'ksf1fl_delta']
ddx_right_knobs = ['ksf1fr_delta', 'ksf2fr_delta', 'ksf2br3_delta',
                   'ksf1br3_delta', 'ksf1ar3_delta', 'ksf2ar3_delta']

tw_no_ip_sext = section.twiss(init=twinit_cell_1_r,
                    compute_chromatic_properties=True)

opt_w_left = section.match(
    name='w_left',
    solve=False,
    init=twinit_cell_1_r,
    compute_chromatic_properties=True,
    vary=xt.VaryList(['ksfx1l', 'ksdy1l'], step=1e-3),
    targets=xt.TargetSet(wx_chrom=0, wy_chrom=0, at='ip_mid')
)
opt = opt_w_left
opt.step(20)

# Match from right to left
opt_w_right = section.match(
    name='w_right',
    solve=False,
    init=twinit_cell_2_l,
    compute_chromatic_properties=True,
    vary=xt.VaryList(['ksfx1r', 'ksdy1r'], step=1e-3),
    targets=xt.TargetSet(wx_chrom=0, wy_chrom=0, at='ip_mid')
)
opt = opt_w_right
opt.step(20)

opt_close_w = section.match(
    name='close',
    solve=False,
    init=twinit_cell_1_r,
    compute_chromatic_properties=True,
    vary=xt.VaryList(['ksfx1l', 'ksdy1l', 'ksfx1r', 'ksdy1r'], step=1e-3),
    targets=[xt.TargetSet(ax_chrom=twinit_cell_1_r.ax_chrom,
                         ay_chrom=twinit_cell_1_r.ay_chrom,
                         bx_chrom=twinit_cell_1_r.bx_chrom,
                         by_chrom=twinit_cell_1_r.by_chrom,
                         at=xt.END),
            xt.TargetSet(wx_chrom=xt.LessThan(10), wy_chrom=xt.LessThan(10),
                         at='ip_mid')]
)
opt = opt_close_w
opt.step(20)

tw_om = twiss_off_momentum(section=section)

# Match third order chromaticity
opt_chrom3_y_left = section.match(
    name='chrom3_l_y',
    solve=False,
    vary=xt.VaryList(['ksdm1l'], step=1e-3, limits=[-0.5, 0.5]),
    targets=[
        act.target('dmuy_l', xt.LessThan(0.1), tol=0.01, weight=1e4, tag='dmuy_l'),
        act.target('dmuy_l', xt.GreaterThan(-0.1), tol=0.01, weight=1e4, tag='dmux_l'),
        act.target('d3muy_l', xt.LessThan(1e3), tol=1, weight=1, tag='d3muy_l'),
        act.target('d3muy_l', xt.GreaterThan(-1e3), tol=1, weight=1, tag='d3muy_l'),
        act.target('muy_rms_l', xt.LessThan(0.05), tol=0.1, weight=1e6, tag='muy_rms_l'),
    ]
)
opt = opt_chrom3_y_left
opt.step(6)
# env['ksdm1l'] = line0['ksdm1l']

opt_chrom3_x_left = section.match(
    name='chrom3_l_x',
    solve=False,
    vary=xt.VaryList(['ksfm2l'], step=1e-3, limits=[-0.5, 0.5]),
    targets=[
        act.target('dmux_l', xt.LessThan(0.1), tol=0.01, weight=1e4, tag='dmux_l'),
        act.target('dmux_l', xt.GreaterThan(-0.1), tol=0.01, weight=1e4, tag='dmux_l'),
        act.target('d3mux_l', xt.LessThan(1e3), tol=1, weight=1, tag='d3mux_l'),
        act.target('d3mux_l', xt.GreaterThan(-1e3), tol=1, weight=1, tag='d3mux_l'),
        act.target('mux_rms_l', xt.LessThan(0.05), tol=0.1, weight=1e6, tag='mux_rms_l'),
    ]
)
opt = opt_chrom3_x_left
opt.step(6)
# env['ksfm2l'] = line0['ksfm2l']

opt_chrom3_y_right = section.match(
    name='chrom3_r_y',
    solve=False,
    vary=xt.VaryList(['ksdm1r'], step=1e-3, limits=[-0.5, 0.5]),
    targets=[
        act.target('dmuy_r', xt.LessThan(1), tol=0.01, weight=1e4, tag='dmuy_r'),
        act.target('dmuy_r', xt.GreaterThan(-1), tol=0.01, weight=1e4, tag='dmuy_r'),
        act.target('d3muy_r', xt.LessThan(3e3), tol=1, weight=1, tag='d3muy_r'),     # For some reason this givea a better behaviour in the closed twiss
        act.target('d3muy_r', xt.GreaterThan(-3e3), tol=1, weight=1, tag='d3muy_r'), # Allowing to go to delta 1.5e-2
        act.target('muy_rms_r', xt.LessThan(0.05), tol=0.1, weight=1e6, tag='muy_rms_r'),
    ]
)
opt = opt_chrom3_y_right
opt.step(6)

opt_chrom3_x_right = section.match(
    name='chrom3_r_x',
    solve=False,
    vary=xt.VaryList(['ksfm2r'], step=1e-3, limits=[-0.5, 0.5]),
    targets=[
        act.target('dmux_r', xt.LessThan(0.1), tol=0.01, weight=1e4, tag='dmux_r'),
        act.target('dmux_r', xt.GreaterThan(-0.1), tol=0.01, weight=1e4, tag='dmux_r'),
        act.target('d3mux_r', xt.LessThan(1e3), tol=1, weight=1, tag='d3mux_r'),
        act.target('d3mux_r', xt.GreaterThan(-1e3), tol=1, weight=1, tag='d3mux_r'),
        act.target('mux_rms_r', xt.LessThan(0.05), tol=0.1, weight=1e6, tag='mux_rms_r'),
    ]
)
opt = opt_chrom3_x_right
opt.step(6)
# env['ksfm2r'] = line0['ksfm2r']


tw_corr_om = twiss_off_momentum(section=section)




opt_ddx_left = section.match(
    name='ddx_left',
    solve=False,
    init=twinit_cell_1_r,
    compute_chromatic_properties=True,
    vary=xt.VaryList(ddx_left_knobs, step=1e-4),
    targets=xt.TargetSet(ddx=0, ddpx=-0, at='ip_mid')
)
opt = opt_ddx_left
opt.step(5)

opt_ddx_right = section.match(
    name='ddx_right',
    solve=False,
    init=twinit_cell_2_l,
    compute_chromatic_properties=True,
    vary=xt.VaryList(ddx_right_knobs, step=1e-4),
    targets=[
        xt.TargetSet(ddx=0, ddpx=0, at='ip_mid'),
        # xt.TargetSet(ddx=xt.GreaterThan(0), at='qdm2r'),
        # xt.TargetSet(ddx=xt.LessThan(3), at='qdm2r')
    ]
)
opt = opt_ddx_right
opt.step(5)

opt = opt_close_w.clone(name='close_final').step(5)

opt_close_w_and_ddx = opt_close_w.clone(name='close_w_and_ddx',
                    remove_vary=True,
                    add_vary=list(opt_ddx_left.vary) + list(opt_ddx_right.vary),
                    add_targets=[
                    xt.TargetSet(
                        ddx=0, ddpx=0, at='ip_mid'),
                    xt.TargetSet(
                         ddx=twinit_cell_1_r.ddx,
                         ddpx=twinit_cell_1_r.ddpx,
                         at=xt.END),
                                ])
opt = opt_close_w_and_ddx
opt.step(5)

prrrr

# Test
# opt.disable(target='ip.*')
# opt.step(5)

tw_om_chrom3 = twiss_off_momentum(section=section)

opt_chrom5_left = section.match(
    name='chrom5_l',
    solve=False,
    init=twinit_cell_1_r,
    compute_chromatic_properties=True,
    vary=xt.VaryList(['kdec1l', 'kdecfl', 'kdecdl'], step=1.),
    targets=[
        act.target('d5mux_l', 0, tol=1e6),
        act.target('d5muy_l', 0, tol=1e6),
    ]
)
opt = opt_chrom5_left
opt.step(10)

opt_chrom5_right = section.match(
    name='chrom5_r',
    solve=False,
    init=twinit_cell_2_l,
    compute_chromatic_properties=True,
    vary=xt.VaryList(['kdec1r', 'kdecfr', 'kdecdr'], step=1.),
    targets=[
        act.target('d5mux_r', 0, tol=1e6),
        act.target('d5muy_r', 0, tol=1e6),
    ]
)
opt = opt_chrom5_right
opt.step(10)

opt_chrom3_x_left.step(5)
opt_chrom3_y_left.step(5)
opt_chrom3_x_right.step(5)
opt_chrom3_y_right.step(5)

# Try to match the chromaticities using the arc families
opt_dqxy = env['fccee_p_ring'].match(
    solve=False,
    method='4d',
    vary=xt.VaryList(['ksffam1', 'ksffam2', 'ksdfam1', 'ksdfam2'], step=1e-3),
    targets=xt.TargetSet(dqx=0, dqy=0, tol=1e-3)
)
opt = opt_dqxy
opt.step(10)


tw_om_final = twiss_off_momentum(section=section)

tw_om_final_full = twiss_off_momentum(section=section,
                                delta_range=(-2e-2, 2e-2), num_delta=41,
                                edge_l=0,edge_r=-1)
# tw_vs_delta = line.get_non_linear_chromaticity(delta0_range=(-1e-2, 1e-2), num_delta=50)

import matplotlib.pyplot as plt
plt.close('all')
spx_l = plt.subplot(2, 2, 1)
spx_r = plt.subplot(2, 2, 2)
spy_l = plt.subplot(2, 2, 3)
spy_r = plt.subplot(2, 2, 4)

spx_l.plot(tw_om['delta_test'], tw_om['mux_l_test'])
spx_l.plot(tw_om['delta_test'], tw_om_chrom3['mux_l_test'])
spx_l.plot(tw_om_final['delta_test'], tw_om_final['mux_l_test'])
spx_l.plot(tw_om['delta_test'], tw0_om['mux_l_test'], '--k')

spx_r.plot(tw_om['delta_test'], tw_om['mux_r_test'])
spx_r.plot(tw_om['delta_test'], tw_om_chrom3['mux_r_test'])
spx_r.plot(tw_om_final['delta_test'], tw_om_final['mux_r_test'])
spx_r.plot(tw_om['delta_test'], tw0_om['mux_r_test'], '--k')

spy_l.plot(tw_om['delta_test'], tw_om['muy_l_test'])
spy_l.plot(tw_om['delta_test'], tw_om_chrom3['muy_l_test'])
spy_l.plot(tw_om_final['delta_test'], tw_om_final['muy_l_test'])
spy_l.plot(tw_om['delta_test'], tw0_om['muy_l_test'], '--k')

spy_r.plot(tw_om['delta_test'], tw_om['muy_r_test'])
spy_r.plot(tw_om['delta_test'], tw_om_chrom3['muy_r_test'])
spy_r.plot(tw_om_final['delta_test'], tw_om_final['muy_r_test'])
spy_r.plot(tw_om['delta_test'], tw0_om['muy_r_test'], '--k')

plt.figure(2)
spx_l = plt.subplot(2, 2, 1)
spx_r = plt.subplot(2, 2, 2)
spy_l = plt.subplot(2, 2, 3)
spy_r = plt.subplot(2, 2, 4)

spx_l.plot(tw_om_final_full['delta_test'], tw_om_final_full['mux_l_test'])
spx_l.plot(tw0_om_full['delta_test'], tw0_om_full['mux_l_test'], '--k')

spx_r.plot(tw_om_final_full['delta_test'], tw_om_final_full['mux_r_test'])
spx_r.plot(tw0_om_full['delta_test'], tw0_om_full['mux_r_test'], '--k')

spy_l.plot(tw_om_final_full['delta_test'], tw_om_final_full['muy_l_test'])
spy_l.plot(tw0_om_full['delta_test'], tw0_om_full['muy_l_test'], '--k')

spy_r.plot(tw_om_final_full['delta_test'], tw_om_final_full['muy_r_test'])
spy_r.plot(tw0_om_full['delta_test'], tw0_om_full['muy_r_test'], '--k')

# # Compare
# tw_ref = line0.twiss4d(delta0=1e-2)
# tw_test = line.twiss4d(delta0=1e-2)

# tw_ref.plot('wx_chrom wy_chrom')
# plt.suptitle('Reference')
# tw_test.plot('wx_chrom wy_chrom')
# plt.suptitle('Test')

plt.show()

