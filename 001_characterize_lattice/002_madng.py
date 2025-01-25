import xtrack as xt

env = xt.Environment()

env.call('../fccee_z_lattice.py')
env.call('../fccee_z_strengths.py')

# Problematic expressions:
env["kcrabl"] = env["kcrabl"] # Set by value
env["kdecdl"] = env["kdecdl"] # Set by value
env["kdecdr"] = env["kdecdr"] # Set by value
env["ksdm1l"] = env["ksdm1l"] # Set by value
env["ksdm1r"] = env["ksdm1r"] # Set by value

line = env.fccee_p_ring

tw = line.twiss4d()

mng = line.to_madng(keep_files=True, temp_fname='ttt', mode='line')