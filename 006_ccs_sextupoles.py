import xtrack as xt
import numpy as np

env = xt.Environment()
env.particle_ref = xt.Particles(mass0=xt.ELECTRON_MASS_EV, energy0=45.6e9)
env.call('fccee_z_parameters.py')
env.call('fccee_z_elements.py')
env.call('fccee_z_lattice.py')
env.call('fccee_z_strengths.py')

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

tw0 = section.twiss(init=twinit_cell_1_r,
                    compute_chromatic_properties=True,
                    strengths=True)
tw0_vs_delta = line.get_non_linear_chromaticity(delta0_range=(-1e-2, 1e-2), num_delta=50)
tt0 = section.get_table(attr=True)
tt0_quad = tt0.rows[tt0.element_type == 'Quadrupole']
tt0_sext = tt0.rows[tt0.element_type == 'Sextupole']

tt_mult_before = env.vars.get_table().rows['koct.*|kdec.*']

for kk in tt_mult_before.name:
    env[kk] = 0.

def twiss_off_momentum():
    delta_test = np.linspace(-0.02, 0.02, 21)
    tw_test = []
    mux_l_test = []
    muy_l_test = []
    mux_r_test = []
    muy_r_test = []
    tt_0 = section.twiss(init_at='ip_mid', betx=env['bxip'], bety=env['byip'])

    for dd in delta_test:
        tt = section.twiss(init_at='ip_mid', betx=env['bxip'], bety=env['byip'],
                        delta=dd)
        mux_l_test.append(tt['mux', 'ip_mid'] - tt['mux', 'ff_edge_l']
                        -(tt_0['mux', 'ip_mid'] - tt_0['mux', 'ff_edge_l']))
        muy_l_test.append(tt['muy', 'ip_mid'] - tt['muy', 'ff_edge_l']
                        -(tt_0['muy', 'ip_mid'] - tt_0['muy', 'ff_edge_l']))
        mux_r_test.append(-tt['mux', 'ip_mid'] + tt['mux', 'ff_edge_r']
                        -(-tt_0['mux', 'ip_mid'] + tt_0['mux', 'ff_edge_r']))
        muy_r_test.append(-tt['muy', 'ip_mid'] + tt['muy', 'ff_edge_r']
                        -(-tt_0['muy', 'ip_mid'] + tt_0['muy', 'ff_edge_r']))
        # mux_l_test.append(tt['mux', 'ff_edge_l'])
        # muy_l_test.append(tt['muy', 'ff_edge_l'])
        # mux_r_test.append(tt['mux', 'ff_edge_r'])
        # muy_r_test.append(tt['muy', 'ff_edge_r'])

        tw_test.append(tt)

    # Polynominal fit
    n_order = 20
    mux_l_test = np.array(mux_l_test)
    muy_l_test = np.array(muy_l_test)
    mux_r_test = np.array(mux_r_test)
    muy_r_test = np.array(muy_r_test)
    delta_test = np.array(delta_test)

    p_mux_l = np.polyfit(delta_test, mux_l_test, n_order)
    p_muy_l = np.polyfit(delta_test, muy_l_test, n_order)
    p_mux_r = np.polyfit(delta_test, mux_r_test, n_order)
    p_muy_r = np.polyfit(delta_test, muy_r_test, n_order)

    mux_l_poly = np.polyval(p_mux_l, delta_test)
    muy_l_poly = np.polyval(p_muy_l, delta_test)
    mux_r_poly = np.polyval(p_mux_r, delta_test)
    muy_r_poly = np.polyval(p_muy_r, delta_test)

    # derivatives in zero
    dmux_l = p_mux_l[-2]
    d2mux_l = 2*p_mux_l[-3]
    d3mux_l = 6*p_mux_l[-4]
    d4mux_l = 24*p_mux_l[-5]
    d5mux_l = 120*p_mux_l[-6]
    dmuy_l = p_muy_l[-2]
    d2muy_l = 2*p_muy_l[-3]
    d3muy_l = 6*p_muy_l[-4]
    d4muy_l = 24*p_muy_l[-5]
    d5muy_l = 120*p_muy_l[-6]

    dmux_r = p_mux_r[-2]
    d2mux_r = 2*p_mux_r[-3]
    d3mux_r = 6*p_mux_r[-4]
    d4mux_r = 24*p_mux_r[-5]
    d5mux_r = 120*p_mux_r[-6]
    dmuy_r = p_muy_r[-2]
    d2muy_r = 2*p_muy_r[-3]
    d3muy_r = 6*p_muy_r[-4]
    d4muy_r = 24*p_muy_r[-5]
    d5muy_r = 120*p_muy_r[-6]
    out = dict(mux_l_test=mux_l_test, muy_l_test=muy_l_test, mux_r_test=mux_r_test, muy_r_test=muy_r_test,
               tw_test=tw_test, delta_test=delta_test,
                p_mux=p_mux_l, p_muy=p_muy_l, tt_0=tt_0,
                mux_l_poly=mux_l_poly, muy_l_poly=muy_l_poly, mux_r_poly=mux_r_poly, muy_r_poly=muy_r_poly,
                dmux_l=dmux_l, d2mux_l=d2mux_l, d3mux_l=d3mux_l, d4mux_l=d4mux_l, d5mux_l=d5mux_l,
                dmuy_l=dmuy_l, d2muy_l=d2muy_l, d3muy_l=d3muy_l, d4muy_l=d4muy_l, d5muy_l=d5muy_l,
                dmux_r=dmux_r, d2mux_r=d2mux_r, d3mux_r=d3mux_r, d4mux_r=d4mux_r, d5mux_r=d5mux_r,
                dmuy_r=dmuy_r, d2muy_r=d2muy_r, d3muy_r=d3muy_r, d4muy_r=d4muy_r, d5muy_r=d5muy_r,
                )

    return out

tw0_om = twiss_off_momentum()

class ActionOffMom(xt.Action):
    def run(self):
        tw_om = twiss_off_momentum()
        return tw_om

act = ActionOffMom()

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


# wipe sextupoles
for kk in ['ksfx1l', 'ksdy1l', 'ksdm1l', 'ksfm2l',
           'ksfx1r', 'ksdy1r', 'ksdm1r', 'ksfm2r',
           ]:
    env[kk] = 0.001 * np.sign(env[kk])

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

tw_om = twiss_off_momentum()



# Match third order chromaticity
opt_chrom3_left = section.match(
    name='chrom_l',
    solve=False,
    init=twinit_cell_1_r,
    compute_chromatic_properties=True,
    vary=xt.VaryList(['ksdm1l', 'ksfm2l'], step=1e-3),
    targets=[
        act.target('d3mux_l', 0, tol=0.1),
        act.target('d3muy_l', 0, tol=0.1),
    ]
)
opt = opt_chrom3_left
opt.step(10)

opt_chrom3_right = section.match(
    name='chrom_r',
    solve=False,
    init=twinit_cell_2_l,
    compute_chromatic_properties=True,
    vary=xt.VaryList(['ksdm1r', 'ksfm2r'], step=1.),
    targets=[
        act.target('d3mux_r', 0, tol=1),
        act.target('d3muy_r', 0, tol=1),
    ]
)
opt = opt_chrom3_right
opt.step(10)

tw_corr_om = twiss_off_momentum()



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

# sf2al3 vars['ksf2al3'] (vars['ksffam2'] + 0.012)
# sd1al3 vars['ksd1al3'] vars['ksdfam1']
# sf1al3 vars['ksf1al3'] ((vars['ksffam1'] + 0.012) + 0.0)
# sd2al3 vars['ksd2al3'] (vars['ksdfam2'] + 0.0)
# sd2bl3 vars['ksd2bl3'] (vars['ksdfam2'] + 0.0)
# sf1bl3 vars['ksf1bl3'] (vars['ksffam1'] - 0.012)
# sd1bl3 vars['ksd1bl3'] (vars['ksdfam1'] - 0.0)
# sf2bl3 vars['ksf2bl3'] ((vars['ksffam2'] - 0.012) - 0.0)
# sf2afl vars['ksf2fl'] (vars['ksffam2'] * 0.6)
# sd1afl vars['ksd1fl'] (vars['ksdfam1'] - 0.0)
# sf1afl vars['ksf1fl'] (vars['ksffam1'] * 0.6)
# sd2afl vars['ksd2fl'] (vars['ksdfam2'] * 0.0)
# sf3afl vars['ksf3fl'] None
# sf3afr vars['ksf3fr'] None
# sd2afr vars['ksd2fr'] (vars['ksdfam2'] * 0.0)
# sf1afr vars['ksf1fr'] (vars['ksffam1'] * 0.6)
# sd1afr vars['ksd1fr'] (vars['ksdfam1'] - 0.0)
# sf2afr vars['ksf2fr'] (vars['ksffam2'] * 0.6)
# sf2br3 vars['ksf2br3'] ((vars['ksffam2'] - 0.012) + 0.0)
# sd1br3 vars['ksd1br3'] (vars['ksdfam1'] - 0.0)
# sf1br3 vars['ksf1br3'] (vars['ksffam1'] - 0.012)
# sd2br3 vars['ksd2br3'] (vars['ksdfam2'] + 0.0)
# sd2ar3 vars['ksd2ar3'] (vars['ksdfam2'] + 0.0)
# sf1ar3 vars['ksf1ar3'] ((vars['ksffam1'] + 0.012) - 0.0)
# sd1ar3 vars['ksd1ar3'] vars['ksdfam1']
# sf2ar3 vars['ksf2ar3'] (vars['ksffam2'] + 0.012)

env.vars.default_to_zero = True
env['ksf2al3'] = 'ksffam2 + ksf2al3_delta'
env['ksf1al3'] = 'ksffam1 + ksf1al3_delta'
env['ksf1bl3'] = 'ksffam1 + ksf1bl3_delta'
env['ksf2bl3'] = 'ksffam2 + ksf2bl3_delta'
env['ksf2fl']  = 'ksffam2 + ksf2fl_delta'
env['ksf1fl']  = 'ksffam1 + ksf1fl_delta'
env['ksf1fr']  = 'ksffam1 + ksf1fr_delta'
env['ksf2fr']  = 'ksffam2 + ksf2fr_delta'
env['ksf2br3'] = 'ksffam2 + ksf2br3_delta'
env['ksf1br3'] = 'ksffam1 + ksf1br3_delta'
env['ksf1ar3'] = 'ksffam1 + ksf1ar3_delta'
env['ksf2ar3'] = 'ksffam2 + ksf2ar3_delta'
env.vars.default_to_zero = False

ddx_left_knobs = ['ksf2al3_delta', 'ksf1al3_delta', 'ksf1bl3_delta',
                  'ksf2bl3_delta', 'ksf2fl_delta', 'ksf1fl_delta']
ddx_right_knobs = ['ksf1fr_delta', 'ksf2fr_delta', 'ksf2br3_delta',
                   'ksf1br3_delta', 'ksf1ar3_delta', 'ksf2ar3_delta']

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

opt_close_w.clone(name='close_final').step(5)
opt_chrom3_left.clone(name='chrom3_left_final').step(5)
opt_chrom3_right.clone(name='chrom3_right_final').step(5)
tw_om_chrom3 = twiss_off_momentum()

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

# Try to match the chromaticities using the arc families
opt_dqxy = env['fccee_p_ring'].match(
    solve=False,
    method='4d',
    vary=xt.VaryList(['ksffam1', 'ksffam2', 'ksdfam1', 'ksdfam2'], step=1e-3),
    targets=xt.TargetSet(dqx=0, dqy=0, tol=1e-3)
)
opt = opt_dqxy
opt.step(10)

tw_om_final = twiss_off_momentum()
# tw_vs_delta = line.get_non_linear_chromaticity(delta0_range=(-1e-2, 1e-2), num_delta=50)

import matplotlib.pyplot as plt
plt.close('all')
spx_l = plt.subplot(2, 2, 1)
spx_r = plt.subplot(2, 2, 2)
spy_l = plt.subplot(2, 2, 3)
spy_r = plt.subplot(2, 2, 4)

spx_l.plot(tw_om['delta_test'], tw_om['mux_l_test'])
spx_l.plot(tw_om['delta_test'], tw_om_chrom3['mux_l_test'])
spx_l.plot(tw_om['delta_test'], tw_om_final['mux_l_test'])
spx_l.plot(tw_om['delta_test'], tw0_om['mux_l_test'], '--k')

spx_r.plot(tw_om['delta_test'], tw_om['mux_r_test'])
spx_r.plot(tw_om['delta_test'], tw_om_chrom3['mux_r_test'])
spx_r.plot(tw_om['delta_test'], tw_om_final['mux_r_test'])
spx_r.plot(tw_om['delta_test'], tw0_om['mux_r_test'], '--k')

spy_l.plot(tw_om['delta_test'], tw_om['muy_l_test'])
spy_l.plot(tw_om['delta_test'], tw_om_chrom3['muy_l_test'])
spy_l.plot(tw_om['delta_test'], tw_om_final['muy_l_test'])
spy_l.plot(tw_om['delta_test'], tw0_om['muy_l_test'], '--k')

spy_r.plot(tw_om['delta_test'], tw_om['muy_r_test'])
spy_r.plot(tw_om['delta_test'], tw_om_chrom3['muy_r_test'])
spy_r.plot(tw_om['delta_test'], tw_om_final['muy_r_test'])
spy_r.plot(tw_om['delta_test'], tw0_om['muy_r_test'], '--k')




plt.show()

