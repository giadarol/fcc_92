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
tw = line.twiss4d()


# sequence_name = 'seq'
# if line.tracker is None:
#     line.build_tracker()
# mng = line.to_madng(sequence_name=sequence_name)
# mng._sequence_name = sequence_name
# line.tracker._madng = mng
# line.tracker._madng_vars = xt.madng_interface.MadngVars(mng)
# line.vars.vars_to_update.add(line.tracker._madng_vars)
# mng = line.tracker._madng

mng = xt.madng_interface.build_madng_model(line, sequence_name='seq')

# line.build_madng_model()
# mng = line.tracker._madng

# mng = line.to_madng(sequence_name='seq')#, temp_fname='ttt', keep_files=True)


mng.send('''
local damap in MAD
local seq = MADX.seq
''')

mng["mytwtable", 'mytwflow'] = mng.twiss(
    sequence=mng.seq, method=4, mapdef=2, implicit=True, nslice=3, save="'atbody'")
