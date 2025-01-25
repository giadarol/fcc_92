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

line = env.fccee_p_ring.copy(shallow=True)
line.replace_all_repeated_elements()
line.build_madng_model()

tw = line.twiss4d()

mng = line.to_madng(sequence_name='seq')#, temp_fname='ttt', keep_files=True)

mng.send('''
local damap in MAD
local seq = MADX.seq
''')

mng["mytwtable", 'mytwflow'] = mng.twiss(
    sequence=mng.seq, method=4, mapdef=2, implicit=True, nslice=3, save="'atbody'")
