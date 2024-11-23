import xtrack as xt
import xobjects as xo
from cpymad.madx import Madx

mad = Madx()
mad.call('../../fcc-ee-lattice/lattices/z/fccee_z.seq')
mad.beam()
mad.use('ring_full')

line_ref = xt.Line.from_madx_sequence(mad.sequence.ring_full, deferred_expressions=True)
line_ref.particle_ref = xt.Particles(mass0=xt.ELECTRON_MASS_EV, energy0=45.6e9)
line_ref.build_tracker()

tw_ref = line_ref.twiss4d(strengths=True)

env = xt.Environment()
env.call('fccee_z_parameters.py')
env.call('fccee_z_elements.py')
env.call('fccee_z_lattice.py')
env.call('fccee_z_strengths.py')

# tw_test = env['ring_full'].twiss4d(betx=tw_ref['betx', 0], bety=tw_ref['bety', 0],
#                                    _continue_if_lost=True)
tw_test = env['ring_full'].twiss4d(strengths=True)

tw_quads_ref = tw_ref.rows[abs(tw_ref.k1l) > 0.0]
tw_quads = tw_test.rows[abs(tw_test.k1l) > 0.0]

import matplotlib.pyplot as plt
plt.close('all')

# Plot beta beat
plt.figure(1)
ax1 = plt.subplot(211)
plt.plot(tw_quads.s, tw_quads.betx/tw_quads_ref.betx-1)
plt.ylabel(r'$\Delta\beta_x / \beta_x$')
plt.subplot(212, sharex=ax1)
plt.plot(tw_quads.s, tw_quads.bety/tw_quads_ref.bety-1)
plt.ylabel(r'$\Delta\beta_y / \beta_y$')
plt.xlabel('s [m]')

plt.figure(2)
ax1 = plt.subplot(211)
plt.plot(tw_quads.s, tw_quads.wx_chrom)
plt.plot(tw_quads.s, tw_quads_ref.wx_chrom)
plt.subplot(212, sharex=ax1)
plt.plot(tw_quads.s, tw_quads.wy_chrom)
plt.plot(tw_quads.s, tw_quads_ref.wy_chrom)

plt.show()