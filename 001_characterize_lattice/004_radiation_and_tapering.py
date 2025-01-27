import matplotlib.pyplot as plt

import xtrack as xt

env = xt.Environment.from_json('fccee_p_ring.json.gz')
line = env.fccee_p_ring_thin

line['rf_lag'] = 0.5
# Leave only one cavity
line.remove('rfc.0')
line.remove('rfc.2')
line.remove('rfc.3')

line['rf_voltage'] = 200.

tt = line.get_table()
tt_cav = tt.rows[tt.element_type == 'Cavity']

tw0 = line.twiss4d()

line.configure_radiation(model='mean')
line.compensate_radiation_energy_loss()
tw = line.twiss(eneloss_and_damping=True)

plt.close('all')
tw.plot('delta')
plt.show()

print(f'Qx thin:  {tw.qx}')
print(f'Qy thin:  {tw.qy}')