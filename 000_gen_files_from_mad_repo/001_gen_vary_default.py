import xtrack as xt

env = xt.Environment()
env.call('../fccee_z_strengths.py')

vary_default = {}

tt_vars = env.vars.get_table()
tt_kq = tt_vars.rows['kq.*']

for nn in tt_kq.name:
    vv = env[nn]
    vary_default[nn]={}
    if vv >= 0:
        vary_default[nn]['limits'] = (0., 10.)
    else:
        vary_default[nn]['limits'] = (-10., 0.)

at_start_file = []
at_start_file.append('import xtrack as xt')
at_start_file.append('env = xt.get_environment()')
at_start_file.append('\ndefault = env.vars.vary_default\n')

out_quad_limits = []
for nn in sorted(list(tt_kq.name)):
    out_quad_limits.append(
        f'default["{nn}"] = ' + '{"limits": ' + str(vary_default[nn]["limits"]) + '}')

with open('quad_strength_limits.py', 'w') as fid:
    fid.write('\n'.join(at_start_file + out_quad_limits))

import shutil
shutil.copy('quad_strength_limits.py', '../002_design_optics')