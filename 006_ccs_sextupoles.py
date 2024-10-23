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

tw_cell_1 = cell1.twiss4d()
twinit_cell_1_r = tw_cell_1.get_twiss_init('mid_cell_edge_r')
tw_cell_2 = cell2.twiss4d()
twinit_cell_2_l = tw_cell_1.get_twiss_init('mid_cell_edge_l')

tw0 = section.twiss(init=twinit_cell_1_r,
                    compute_chromatic_properties=True)


def twiss_off_momentum():
    delta_test = np.linspace(-0.03, 0.03, 21)
    tw_test = []
    mux_l_test = []
    muy_l_test = []
    tt_0 = section.twiss(init_at='ip_mid', betx=env['bxip'], bety=env['byip'])

    for dd in delta_test:
        tt = section.twiss(init_at='ip_mid', betx=env['bxip'], bety=env['byip'],
                        delta=dd)
        mux_l_test.append(tt['mux', 'ip_mid'] - tt['mux', 'ff_edge_l']
                        -(tt_0['mux', 'ip_mid'] - tt_0['mux', 'ff_edge_l']))
        muy_l_test.append(tt['muy', 'ip_mid'] - tt['muy', 'ff_edge_l']
                        -(tt_0['muy', 'ip_mid'] - tt_0['muy', 'ff_edge_l']))

        tw_test.append(tt)

    # Polynominal fit
    n_order = 10
    mux_l_test = np.array(mux_l_test)
    muy_l_test = np.array(muy_l_test)
    delta_test = np.array(delta_test)
    p_mux = np.polyfit(delta_test, mux_l_test, n_order)
    p_muy = np.polyfit(delta_test, muy_l_test, n_order)

    mux_l_poly = np.polyval(p_mux, delta_test)
    muy_l_poly = np.polyval(p_muy, delta_test)

    # derivative in zero
    dmux = p_mux[-2]
    d2mux = 2*p_mux[-3]
    d3mux = 6*p_mux[-4]
    d4mux = 24*p_mux[-5]
    d5mux = 120*p_mux[-6]
    dmuy = p_muy[-2]
    d2muy = 2*p_muy[-3]
    d3muy = 6*p_muy[-4]
    d4muy = 24*p_muy[-5]
    d5muy = 120*p_muy[-6]

    out = dict(mux_l_test=mux_l_test, muy_l_test=muy_l_test,
               tw_test=tw_test, delta_test=delta_test,
                p_mux=p_mux, p_muy=p_muy,
                mux_l_poly=mux_l_poly, muy_l_poly=muy_l_poly,
                dmux=dmux, d2mux=d2mux, d3mux=d3mux, d4mux=d4mux, d5mux=d5mux,
                dmuy=dmuy, d2muy=d2muy, d3muy=d3muy, d4muy=d4muy, d5muy=d5muy,
                )

    return out

tw0_om = twiss_off_momentum()


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
    vary=xt.VaryList(['ksfx1l', 'ksdy1l'], step=1e-4),
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
    vary=xt.VaryList(['ksfx1r', 'ksdy1r'], step=1e-4),
    targets=xt.TargetSet(wx_chrom=0, wy_chrom=0, at='ip_mid')
)
opt = opt_w_right
opt.step(20)

tw_om = twiss_off_momentum()
