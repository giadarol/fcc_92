import numpy as np
import xtrack as xt

# Needs:
#  - access targets and vary by name
#  - automatic tag generation for targets
#  - add opt.twiss
#  - env.vars.update

env = xt.Environment()
env.call('fccee_z_parameters.py')
env.call('fccee_z_elements.py')
env.call('fccee_z_lattice.py')
env.call('fccee_z_strengths.py')

# Load cell strengths from my match
env.vars.load_json('strengths_quads_00_arc_cell.json')

tw_uu = env['arc_uu'].twiss4d()

line = env['arc_ussu']

tw0 = line.twiss(betx=tw_uu.betx[0], bety=tw_uu.bety[0],
                 alfx=tw_uu.alfx[0], alfy=tw_uu.alfy[0],
                    dx=tw_uu.dx[0], dpx=tw_uu.dpx[0])

kq = {}
kq['ussu'] = [
    'kqfs0', 'kqds0', 'kqfs1', 'kqds2', 'kqfs3', 'kqds4',
    'kqfs5', 'kqdl1', 'kqfl2', 'kqdl2', 'kqfl3', 'kqdl3',
    'kqfl6', 'kqdl4', 'kqfl4', 'kqfl5', 'kqdl5', 'kqdl6']

# Build vary objects keeping the initial signs
vary_kq = {}
for kk in kq.keys():
    vary_kq[kk] = []
    for nn in kq[kk]:
        vv = env[nn]
        vary_kq[kk].append(xt.Vary(nn, step=1e-6,
                    limits={False:(-10, 0.), True:(0., 10.)}[vv>=0.], tag=kk))


tar_bet = [
   xt.TargetSet(at='qfs1a::0', betx=xt.LessThan(140.)),
   xt.TargetSet(at='qfs3a::0', betx=xt.LessThan(140), bety=xt.GreaterThan(25.)),
   xt.TargetSet(at='qfs5a::0', betx=xt.LessThan(190), bety=xt.GreaterThan(25.)),
   xt.TargetSet(at='qfl2a::0', betx=xt.LessThan(260)),
   xt.TargetSet(at='qfl3a::0', betx=xt.LessThan(env['bxmax']), bety=xt.GreaterThan(62)),
   xt.TargetSet(at='qfl6a::0', betx=xt.LessThan(env['bxmax'])),
   xt.TargetSet(at='qfl4a::0', betx=xt.LessThan(env['bxmax']), bety=xt.GreaterThan(65)),
   xt.TargetSet(at='qfl5a::0', betx=xt.LessThan(env['bxmax'])),
   xt.TargetSet(at='qds0a::0', bety=xt.LessThan(155)),
   xt.TargetSet(at='qds2a::0', bety=xt.LessThan(155)),
   xt.TargetSet(at='qds4a::0', bety=xt.LessThan(155)),
   xt.TargetSet(at='qdl1a::0', bety=xt.LessThan(235)),
   xt.TargetSet(at='qdl2a::0', bety=xt.LessThan(env['bymax'])),
   xt.TargetSet(at='qdl3a::0', bety=xt.LessThan(env['bymax'])),
   xt.TargetSet(at='qdl4a::0', bety=xt.LessThan(env['bymax'])),
   xt.TargetSet(at='qdl5a::0', bety=xt.LessThan(env['bymax'])),
   xt.TargetSet(at='qdl5a::0', bety=xt.LessThan(env['bymax']))
]
tar_center = xt.TargetSet(at='scenter::0', betx=env['bxsc'], bety=env['bysc'], dx=0)

tar_end = xt.TargetSet(at=xt.END,
    betx=tw_uu.betx[0], bety=tw_uu.bety[0], alfx=0, alfy=0,
    dx=tw_uu.dx[0], dpx=tw_uu.dpx[0],
    mux = tw_uu.mux[-1] * 0.5 + 3.0,
    muy = tw_uu.muy[-1] * 0.5 + 3.0)

opt_pant = line.match(
    solve=False,
    method='4d',
    vary=vary_kq['ussu'],
    betx=tw_uu.betx[0], bety=tw_uu.bety[0],
    alfx=tw_uu.alfx[0], alfy=tw_uu.alfy[0],
    dx=tw_uu.dx[0], dpx=tw_uu.dpx[0],
    targets=tar_bet + [tar_center, tar_end],
)
