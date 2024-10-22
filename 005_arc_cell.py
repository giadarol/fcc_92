import xtrack as xt

env = xt.Environment()
env.call('fccee_z_parameters.py')
env.call('fccee_z_elements.py')
env.call('fccee_z_lattice.py')
env.call('fccee_z_strengths.py')

line = env['cell_u']
tw0 = line.twiss4d(strengths=True)

tt0 = line.get_table(attr=True)
tt0_quad = tt0.rows[tt0.element_type == 'Quadrupole']
tt0_sext = tt0.rows[tt0.element_type == 'Sextupole']


kq = {}
kq['cell'] = ['kqd1', 'kqf2', 'kqd3', 'kqf4', 'kqd5', 'kqf6']

# Build vary objects keeping the initial signs
vary_kq = {}
for kk in kq.keys():
    vary_kq[kk] = []
    for nn in kq[kk]:
        vv = env[nn]
        vary_kq[kk].append(xt.Vary(nn,
                    limits={False:(-10, 0.), True:(0., 10.)}[vv>=0.], tag=kk))
vary_all = []
for kk in kq.keys():
    vary_all += vary_kq[kk]

opt_pant = line.match(
    solve=False,
    method='4d',
    targets=[
        xt.TargetSet(at=xt.END,
                     mux=env['muxu'], muy=env['muyu'])
    ],
    vary=vary_all,
)
opt = opt_pant