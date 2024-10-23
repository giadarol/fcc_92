import xtrack as xt
import numpy as np

env = xt.Environment()
env.particle_ref = xt.Particles(mass0=xt.ELECTRON_MASS_EV, energy0=45.6e9)
env.call('fccee_z_parameters.py')
env.call('fccee_z_elements.py')
env.call('fccee_z_lattice.py')
env.call('fccee_z_strengths.py')

line = env['fccee_p_ring']
cell1 = line.select('mid_cell_edge_l::1','mid_cell_edge_r::1')

tw_cell_1 = cell1.twiss4d()
twinit_cell_1_r = tw_cell_1.get_twiss_init('mid_cell_edge_r')

section = line.select('mid_cell_edge_r::1','mid_cell_edge_l::2')

tw0 = section.twiss(init=twinit_cell_1_r,
                    compute_chromatic_properties=True)

# wipe sextupoles
for kk in ['ksdy1l', 'ksdy2l', 'ksdm1l', 'ksdm1l', 'ksfm2l',
           'ksfx1l', 'kcrabl']:
    env[kk] = 0.

tw_no_ip_sext = section.twiss(init=twinit_cell_1_r,
                    compute_chromatic_properties=True)