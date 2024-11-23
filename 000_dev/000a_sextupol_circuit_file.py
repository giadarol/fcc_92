import xtrack as xt

env = xt.Environment()
env.call('fccee_z_strengths.py')

tt = env.vars.get_table().rows['k.*']

# Final focus special arc cell sextupoles

env['ksf2al3'] = vars['ksffam2']
env['ksd1al3'] = vars['ksdfam1']
env['ksf1al3'] = vars['ksffam1']
env['ksd2al3'] = vars['ksdfam2']
env['ksd2bl3'] = vars['ksdfam2']
env['ksf1bl3'] = vars['ksffam1']
env['ksd1bl3'] = vars['ksdfam1']
env['ksf2bl3'] = vars['ksffam2']
env['ksf2fl']  = vars['ksffam2']
env['ksd1fl']  = vars['ksdfam1']
env['ksf1fl']  = vars['ksffam1']
env['ksd2fl']  = 0.
env['ksf3fl']  = 0.
env['ksf3fr']  = 0.
env['ksd2fr']  = 0.
env['ksf1fr']  = vars['ksffam1']
env['ksd1fr']  = vars['ksdfam1']
env['ksf2fr']  = vars['ksffam2']
env['ksf2br3'] = vars['ksffam2']
env['ksd1br3'] = vars['ksdfam1']
env['ksf1br3'] = vars['ksffam1']
env['ksd2br3'] = vars['ksdfam2']
env['ksd2ar3'] = vars['ksdfam2']
env['ksf1ar3'] = vars['ksffam1']
env['ksd1ar3'] = vars['ksdfam1']
env['ksf2ar3'] = vars['ksffam2']