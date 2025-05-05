import xtrack as xt
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

env = xt.Environment()
env.call('../fccee_z_lattice.py')
env.call('../fccee_z_strengths.py')

line = env['fccee_p_ring']

# line.survey().plot(element_width=100)

line.insert(
    [
        line.env.new('dummy_quad', 'Quadrupole', length=1., k1=0, at=69230.),
        line.env.new('dummy_sext', 'Sextupole', length=1., k2=0.),
        line.env.new('dummy_bend', 'Bend', length=1., angle=0.),

    ])

tw = line.twiss(strengths=True)
tw_l = line.twiss(strengths=True, zero_at='_end_point')

for tt in [tw, tw_l]:
    tt.k1l = np.sign(tt.k1l)*tt.length
    tt.k2l = np.sign(tt.k2l)*tt.length
    tt['k1l', 'dummy_quad'] = 10
    tt['k2l', 'dummy_sext'] = 5
    tt['k0l', 'dummy_bend'] = 0.001
    tt['angle_rad', 'dummy_quad'] = tt['k0l', 'dummy_bend']

plt.close('all')
plt.figure(1, figsize=(15, 4))
ax = plt.subplot(111)
pp = tw.plot(lattice_only=True, ax=ax)
plt.xlim(0, 1800)
plt.subplots_adjust(left=0.05, right=0.95, bottom=.14)
pp.ylim(lattice_lo=-0.3, lattice_hi=0.3)

plt.figure(2, figsize=(15, 4))
ax = plt.subplot(111)
pp = tw_l.plot(lattice_only=True, ax=ax)
plt.xlim(-1800, 0)
plt.subplots_adjust(left=0.05, right=0.95, bottom=.14)
pp.ylim(lattice_lo=-0.3, lattice_hi=0.3)

plt.show()

