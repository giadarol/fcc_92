import xtrack as xt
import numpy as np


class Starfish(xt.Action):

    def __init__(self, line_starfish, nemitt_x, nemitt_y, n_test=20):
        self.line_starfish = line_starfish
        self.nemitt_x = nemitt_x
        self.nemitt_y = nemitt_y

        self.tw_sf = line_starfish.twiss4d(strengths=True)

        self.p_test_x = line_starfish.build_particles(
            method='4d',
            x_norm=np.linspace(0, 400, n_test),
            y_norm=0,
            nemitt_x=nemitt_x,
            nemitt_y=nemitt_y,
        )

        self.p_test_y = line_starfish.build_particles(
            method='4d',
            x_norm=0,
            y_norm=np.linspace(0, 400, n_test),
            nemitt_x=nemitt_x,
            nemitt_y=nemitt_y,
        )

        self.p_test_xy = line_starfish.build_particles(
            method='4d',
            x_norm=np.linspace(0, 400, n_test),
            y_norm=np.linspace(0, 400, n_test),
            nemitt_x=nemitt_x,
            nemitt_y=nemitt_y,
        )



    def starfish(self, plot=False):

        line_starfish = self.line_starfish
        tw_sf = self.tw_sf
        nemitt_x = self.nemitt_x
        nemitt_y = self.nemitt_y
        p_test_x = self.p_test_x
        p_test_y = self.p_test_y
        p_test_xy = self.p_test_xy

        line_starfish.track(num_turns=6, particles=self.p_test_x.copy(), turn_by_turn_monitor=True)
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

    __call__ = starfish
    run = starfish