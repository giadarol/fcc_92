import xtrack as xt
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

env = xt.Environment()
env.call('../fccee_z_lattice.py')
env.call('../fccee_z_strengths.py')

line = env['fccee_p_ring']

tt = line.get_table(attr=True)

# tw4d = line.twiss4d()
# tw4d.plot()
# tw4d.plot('wx_chrom wy_chrom')
# tw4d.plot('ddx')

# Remove lag (radiation is off)
env['rf_lag'] = 0.5

tw6d = line.twiss()
tw6d.plot()
tw6d.plot('wx_chrom wy_chrom')
tw6d.plot('ddx')
