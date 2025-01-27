import xtrack as xt

line = xt.Line.from_json('fccee_p_ring_thin.json.gz')

line['rf_lag'] = 0.5

line.configure_radiation(model='mean')

line.compensate_radiation_energy_loss()

tw = line.twiss(eneloss_and_damping=True)

tw.plot('delta')

print(f'Qx thin:  {tw.qx}')
print(f'Qy thin:  {tw.qy}')