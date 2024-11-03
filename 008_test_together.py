import xtrack as xt
import numpy as np

env = xt.Environment()
env.call('fccee_z_parameters.py')
env.call('fccee_z_elements.py')
env.call('fccee_z_lattice.py')

line = env['fccee_p_ring']

env.vars.load_json('strengths_quads_00_arc_cell_quad.json')
env.vars.load_json('strengths_quads_01_ffccsyl.json')
env.vars.load_json('strengths_quads_02_ffccsxl.json')
env.vars.load_json('strengths_quads_03_ffccsyr.json')
env.vars.load_json('strengths_quads_04_ffccsxr.json')
env.vars.load_json('strengths_quads_05_ffds_lr.json')

tt = line.get_table(attr=True)

tw = line.twiss(
    start='mid_cell_edge_l::1',
    end='mid_cell_edge_r::2',
    init_at='ip_mid::1',
    betx=env['bxip'],
    bety=env['byip'],
)


