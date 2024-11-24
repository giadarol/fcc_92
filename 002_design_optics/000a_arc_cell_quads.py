import xtrack as xt
import numpy as np

env = xt.Environment()
env.call('../fccee_z_lattice.py')
env.call('quad_strength_limits.py')

env.call('matching_constraints.py')

line = env['cell_u']

tt0 = line.get_table(attr=True)
tt0_quad = tt0.rows[tt0.element_type == 'Quadrupole']
tt0_sext = tt0.rows[tt0.element_type == 'Sextupole']


kq_names = ['kqd1', 'kqf2', 'kqd3', 'kqf4', 'kqd5', 'kqf6']

line['kqd1'] = -1e-2
line['kqf2'] = 1e-2
line['kqd3'] = -1e-2
line['kqf4'] = 1e-2
line['kqd5'] = -1e-2
line['kqf6'] = 1e-2

opt_phase = line.match(
    solve=False,
    method='4d',
    vary=xt.VaryList(kq_names, step=1e-4),
    targets=xt.TargetSet(mux=env['muxu'], muy=env['muyu'], at=xt.END, tol=1e-6)
)
opt_phase.step(10)

qf_entry = ['qf2a::0', 'qf4a::0', 'qf6a',    'qf4a::1', 'qf2a::1']
qd_entry = ['qd3a::0', 'qd5a::0', 'qd5a::1', 'qd3a::1', 'qd1a::1']

opt_cell = opt_phase.clone(name='phase + peaks',
    add_targets=[
        xt.Target(lambda tw: np.std(tw.rows[qf_entry].dx),   xt.LessThan(0.001), tag='dx',   tol=1e-3, weight=1000),
        xt.Target(lambda tw: np.std(tw.rows[qd_entry].bety), xt.LessThan(0.5), tag='bety', tol=1e-3, weight=1),
        xt.Target(lambda tw: np.std(tw.rows[qf_entry].betx), xt.LessThan(0.5), tag='betx', tol=1e-3, weight=1),
])
opt = opt_cell
opt.run_simplex(1000, fatol=1e-10, xatol=1e-3)

opt_cell.tag('final')
xt.json.dump(opt_cell.get_knob_values(-1), 'strengths_quads_00_arc_cell.json')
