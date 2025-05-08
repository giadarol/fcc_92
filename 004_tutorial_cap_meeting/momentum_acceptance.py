import xtrack as xt
from gen_grid import initial_conditions_grid
import matplotlib.pyplot as plt

class ActionMomentumAcceptance(xt.Action):

    def __init__(self, line, nemitt_x, nemitt_y, nn_y_r, max_y_r, energy_spread,
                 num_turns=100,
                 delta_initial_values=None,
                 chrom_knobs=None,
                 chrom_target=None,
                 global_xy_limit=10e-2,
                 opt=None,
                 n_opt_steps=1):
        self.line = line
        self.nemitt_x = nemitt_x
        self.nemitt_y = nemitt_y
        self.nn_y_r = nn_y_r
        self.max_y_r = max_y_r
        self.energy_spread = energy_spread
        self.num_turns = num_turns
        self.chrom_knobs = chrom_knobs
        self.chrom_target = chrom_target
        self.global_xy_limit = global_xy_limit
        self.opt = opt
        self.n_opt_steps = n_opt_steps

        self.tt_init = initial_conditions_grid(
            study='MA',
            nn_y_r=nn_y_r,
            max_y_r=max_y_r,
            energy_spread=energy_spread,
            delta_initial_values=delta_initial_values)

    def mom_acceptance(self, plot=False, with_progress=False):

        line = self.line
        nemitt_x = self.nemitt_x
        nemitt_y = self.nemitt_y
        tt_init = self.tt_init

        if self.opt is not None:
            for nn in self.opt.get_knob_values().keys():
                line[nn] = 0
            oo = self.opt.clone()
            oo._err._force_jacobian = self.opt._err._force_jacobian
            oo.step(self.n_opt_steps)
            oo.target_mismatch()

        if self.chrom_knobs is not None:
            assert self.chrom_target is not None
            tw = line.twiss()
            line[self.chrom_knobs[0]] -= (tw.dqx - self.chrom_target[0])
            line[self.chrom_knobs[1]] -= (tw.dqy - self.chrom_target[1])

        particles = line.build_particles(
            method='4d',
            nemitt_x=nemitt_x, nemitt_y=nemitt_y,
            delta=tt_init.delta_init,
            x_norm=tt_init.x_normalized,
            y_norm=tt_init.y_normalized)
        self.last_particles = particles

        line.config.XTRACK_GLOBAL_XY_LIMIT = self.global_xy_limit
        line.track(particles, num_turns=self.num_turns, with_progress=with_progress)

        particles.sort(interleave_lost_particles=True)
        lost = particles.state <= 0
        frac_lost = lost.sum() / len(lost)
        at_turn_mean = particles.at_turn.mean()
        print(f'frac_lost: {frac_lost:.3g}, at_turn_mean: {at_turn_mean:.6g} <--')

        if plot:
            tt = line.get_table(attr=True)
            sp = plt.subplot(211)
            sp.plot(tt_init.delta_init[~lost], tt_init.x_normalized[~lost], '.')
            # use particles.at_turn as color
            sp.set_xlabel(r'$\delta$')
            sp.set_ylabel(r'$\hat{x}$')
            sp.scatter(tt_init.delta_init[lost], tt_init.x_normalized[lost],
                        c=particles.at_turn[lost], marker='o')
            sp2 = plt.subplot(212)
            sp2.plot(tt.s[:-1], line.attr['k2l'], '.')
            sp2.set_xlabel('s [m]')
            sp2.set_ylabel('k2l [1/m^2]')

            plt.show()

        out = {
            'particles': particles,
            'lost': lost,
            'frac_lost': frac_lost,
            'at_turn_mean': particles.at_turn.mean(),
        }
        return out

    def run(self):
        return self.mom_acceptance()