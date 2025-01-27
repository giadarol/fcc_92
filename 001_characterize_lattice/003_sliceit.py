import xtrack as xt
import numpy as np

env = xt.Environment()

env.call('../fccee_z_lattice.py')
env.call('../fccee_z_strengths.py')

line_thick = env.fccee_p_ring
tw_thick = line_thick.twiss4d(strengths=True)

# Sort quads by beta function
tw_quads = tw_thick.rows[tw_thick.element_type == 'Quadrupole']
bet_max_xy = [(max([tw_quads.betx[ii], tw_quads.bety[ii]]))
              for ii in range(len(tw_quads))]
tw_quads['bet_max_xy'] = np.array(bet_max_xy)
i_sorted = np.argsort(bet_max_xy)
tw_quads_sorted = tw_quads.rows[i_sorted[::-1]]


line = line_thick.copy(shallow=True)

Strategy = xt.slicing.Strategy
Teapot = xt.slicing.Teapot

# Quads with betas above above 2000 m
# qd0bl::0       1057.38       4249.39       4249.39
# qy3l::0        226.316       3893.89       3893.89
# qf1ar::0        1115.8       3831.32       3831.32
# qf1al::0       1325.74       3437.01       3437.01
# qf1bl::0       1331.54       3414.39       3414.39
# qd1l::0        1405.88       3150.57       3150.57
# qf1br::0       1315.17       3066.99       3066.99
# qy2l::0        843.651       2956.75       2956.75
# qf2l::0        2942.48       821.613       2942.48
# qd1r::0        768.307        2134.7        2134.7

slicing_strategies = [
    Strategy(slicing=None),  # Default catch-all as in MAD-X
    Strategy(slicing=Teapot(3), element_type=xt.Bend),
    # Quad with betas above 5000 m
    Strategy(slicing=Teapot(200), name=r'qd0al.*'),
    Strategy(slicing=Teapot(200), name=r'qd0br.*'),
    Strategy(slicing=Teapot(200), name=r'qd6l.*'),
    Strategy(slicing=Teapot(200), name=r'qy1l.*'),
    Strategy(slicing=Teapot(200), name=r'qd7r.*'),
    Strategy(slicing=Teapot(200), name=r'qy1r.*'),
    Strategy(slicing=Teapot(200), name=r'qd7l.*'),
    Strategy(slicing=Teapot(200), name=r'qd6r.*'),
    Strategy(slicing=Teapot(200), name=r'qd0ar.*'),
    # Quads with betas above 2000 m
    Strategy(slicing=Teapot(100), name=r'qd0bl.*'),
    Strategy(slicing=Teapot(100), name=r'qy3l.*'),
    Strategy(slicing=Teapot(100), name=r'qf1ar.*'),
    Strategy(slicing=Teapot(100), name=r'qf1al.*'),
    Strategy(slicing=Teapot(100), name=r'qf1bl.*'),
    Strategy(slicing=Teapot(100), name=r'qd1l.*'),
    Strategy(slicing=Teapot(100), name=r'qf1br.*'),
    Strategy(slicing=Teapot(100), name=r'qy2l.*'),
    Strategy(slicing=Teapot(100), name=r'qf2l.*'),
    Strategy(slicing=Teapot(100), name=r'qd1r.*'),
# qd0ar::0       6913.04
# qd0br::0       8371.59
# qf1ar::0       3831.32
# qf1br::0       3066.99
    # Strategy(slicing=Teapot(50), element_type=xt.Quadrupole), # Starting point
    # Strategy(slicing=Teapot(5), name=r'^qf.*'),
    # Strategy(slicing=Teapot(5), name=r'^qd.*'),
    # Strategy(slicing=Teapot(5), name=r'^qfg.*'),
    # Strategy(slicing=Teapot(5), name=r'^qdg.*'),
    # Strategy(slicing=Teapot(5), name=r'^ql.*'),
    # Strategy(slicing=Teapot(5), name=r'^qs.*'),
    # Strategy(slicing=Teapot(10), name=r'^qb.*'),
    # Strategy(slicing=Teapot(10), name=r'^qg.*'),
    # Strategy(slicing=Teapot(10), name=r'^qh.*'),
    # Strategy(slicing=Teapot(10), name=r'^qi.*'),
    # Strategy(slicing=Teapot(10), name=r'^qr.*'),
    # Strategy(slicing=Teapot(10), name=r'^qu.*'),
    # Strategy(slicing=Teapot(10), name=r'^qy.*'),
    # Strategy(slicing=Teapot(50), name=r'^qa.*'),
    # Strategy(slicing=Teapot(50), name=r'^qc.*'),
    # Strategy(slicing=Teapot(20), name=r'^sy\..*'),
    # Strategy(slicing=Teapot(30), name=r'^mwi\..*'),
]

line.slice_thick_elements(slicing_strategies=slicing_strategies)

tw = line.twiss4d()

print(f'Qx thick: {tw_thick.qx}')
print(f'Qx thin:  {tw.qx}, error: {tw.qx - tw_thick.qx:.2e}')
print(f'Qy thick: {tw_thick.qy}')
print(f'Qy thin:  {tw.qy}, error: {tw.qy - tw_thick.qy:.2e}')


