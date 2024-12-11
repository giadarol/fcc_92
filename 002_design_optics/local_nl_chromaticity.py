import numpy as np
import xtrack as xt

class LocalNonLinearChromaticity(xt.Action):

    def __init__(self, section):
        self.section = section

    def run(self, delta_range=(-0.02, 0.02), num_delta=21,
                            edge_l='ff_edge_l', edge_r='ff_edge_r',
                            plot=False, fig=None):

        section = self.section
        env = section

        delta_test = np.linspace(*delta_range, num_delta)
        tw_test = []
        mux_l_test = []
        muy_l_test = []
        mux_r_test = []
        muy_r_test = []
        tt_0 = section.twiss(init_at='ip_mid', betx=env['bxip'], bety=env['byip'])

        for dd in delta_test:
            tt = section.twiss(init_at='ip_mid', betx=env['bxip'], bety=env['byip'],
                            delta=dd)
            mux_l_test.append(tt['mux', 'ip_mid'] - tt['mux', edge_l]
                            -(tt_0['mux', 'ip_mid'] - tt_0['mux', edge_l]))
            muy_l_test.append(tt['muy', 'ip_mid'] - tt['muy', edge_l]
                            -(tt_0['muy', 'ip_mid'] - tt_0['muy', edge_l]))
            mux_r_test.append(-tt['mux', 'ip_mid'] + tt['mux', edge_r]
                            -(-tt_0['mux', 'ip_mid'] + tt_0['mux', edge_r]))
            muy_r_test.append(-tt['muy', 'ip_mid'] + tt['muy', edge_r]
                            -(-tt_0['muy', 'ip_mid'] + tt_0['muy', edge_r]))
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

        mux_rms_l = mux_l_test.std()
        muy_rms_l = muy_l_test.std()
        mux_rms_r = mux_r_test.std()
        muy_rms_r = muy_r_test.std()
        out = dict(mux_l_test=mux_l_test, muy_l_test=muy_l_test, mux_r_test=mux_r_test, muy_r_test=muy_r_test,
                tw_test=tw_test, delta_test=delta_test,
                    p_mux=p_mux_l, p_muy=p_muy_l, tt_0=tt_0,
                    mux_rms_l=mux_rms_l, muy_rms_l=muy_rms_l, mux_rms_r=mux_rms_r, muy_rms_r=muy_rms_r,
                    mux_l_poly=mux_l_poly, muy_l_poly=muy_l_poly, mux_r_poly=mux_r_poly, muy_r_poly=muy_r_poly,
                    dmux_l=dmux_l, d2mux_l=d2mux_l, d3mux_l=d3mux_l, d4mux_l=d4mux_l, d5mux_l=d5mux_l,
                    dmuy_l=dmuy_l, d2muy_l=d2muy_l, d3muy_l=d3muy_l, d4muy_l=d4muy_l, d5muy_l=d5muy_l,
                    dmux_r=dmux_r, d2mux_r=d2mux_r, d3mux_r=d3mux_r, d4mux_r=d4mux_r, d5mux_r=d5mux_r,
                    dmuy_r=dmuy_r, d2muy_r=d2muy_r, d3muy_r=d3muy_r, d4muy_r=d4muy_r, d5muy_r=d5muy_r,
                    )

        if plot:

            from matplotlib import pyplot as plt
            if fig is None:
                fig = plt.figure()

            tw_om = out

            spx_l = plt.subplot(2, 2, 1)
            spx_r = plt.subplot(2, 2, 2)
            spy_l = plt.subplot(2, 2, 3)
            spy_r = plt.subplot(2, 2, 4)

            spx_l.plot(tw_om['delta_test'], tw_om['mux_l_test'])
            spx_l.plot(tw_om['delta_test'], tw_om['mux_l_poly'], '--')
            spx_l.set_title(f"dmux = {tw_om['dmux_l']:.3e}, "
                            f"d2mux = {tw_om['d2mux_l']:.3e}, "
                            f"d3mux = {tw_om['d3mux_l']:.3e},\n"
                            f"d4mux = {tw_om['d4mux_l']:.3e}, "
                            f"d5mux = {tw_om['d5mux_l']:.3e}")
            spx_r.plot(tw_om['delta_test'], tw_om['mux_r_test'])
            spx_r.plot(tw_om['delta_test'], tw_om['mux_r_poly'], '--')
            spx_r.set_title(f"dmux = {tw_om['dmux_r']:.3e}, "
                            f"d2mux = {tw_om['d2mux_r']:.3e}, "
                            f"d3mux = {tw_om['d3mux_r']:.3e},\n"
                            f"d4mux = {tw_om['d4mux_r']:.3e}, "
                            f"d5mux = {tw_om['d5mux_r']:.3e}")
            spy_l.plot(tw_om['delta_test'], tw_om['muy_l_test'])
            spy_l.plot(tw_om['delta_test'], tw_om['muy_l_poly'], '--')
            spy_l.set_title(f"dmuy = {tw_om['dmuy_l']:.3e}, "
                            f"d2muy = {tw_om['d2muy_l']:.3e}, "
                            f"d3muy = {tw_om['d3muy_l']:.3e},\n"
                            f"d4muy = {tw_om['d4muy_l']:.3e}, "
                            f"d5muy = {tw_om['d5muy_l']:.3e}")
            spy_r.plot(tw_om['delta_test'], tw_om['muy_r_test'])
            spy_r.plot(tw_om['delta_test'], tw_om['muy_r_poly'], '--')
            spy_r.set_title(f"dmuy = {tw_om['dmuy_r']:.3e}, "
                            f"d2muy = {tw_om['d2muy_r']:.3e}, "
                            f"d3muy = {tw_om['d3muy_r']:.3e},\n"
                            f"d4muy = {tw_om['d4muy_r']:.3e}, "
                            f"d5muy = {tw_om['d5muy_r']:.3e}")

        return out
