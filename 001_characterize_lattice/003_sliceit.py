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

# Quads with betas above above 1000 m
# qf8r::0        129.198       1814.78       1814.78
# qy2r::0        432.512       1746.74       1746.74
# qy3r::0        68.3759       1628.46       1628.46
# qdm8r::0        66.671       1599.71       1599.71
# qd20l::0       66.6715       1599.71       1599.71
# qd20r::0       66.9952       1592.45       1592.45
# qdm8l::0        71.838       1483.52       1483.52
# qf8l::0        734.272       1473.86       1473.86
# qx0l::0        1040.71       42.1744       1040.71
# qf12l::0        1040.7       42.2293        1040.7
# qf13l::0       1025.25       42.0447       1025.25

slicing_strategies = [
    Strategy(slicing=None),  # Default catch-all as in MAD-X
    Strategy(slicing=Teapot(2), element_type=xt.Bend),
    Strategy(slicing=Teapot(5), element_type=xt.Quadrupole),
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
]

line.slice_thick_elements(slicing_strategies=slicing_strategies)

tw = line.twiss4d(strengths=True)

print(f'Qx thick: {tw_thick.qx}')
print(f'Qx thin:  {tw.qx}, error: {tw.qx - tw_thick.qx:.2e}')
print(f'Qy thick: {tw_thick.qy}')
print(f'Qy thin:  {tw.qy}, error: {tw.qy - tw_thick.qy:.2e}')


