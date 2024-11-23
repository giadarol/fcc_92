# Other lines used for matching
env['mccs_yl'] = -env['ccs_yl']
env['mccs_yxl'] = -env['ccs_yl'] + (-env['ccs_xl'])
env['ccs_yxl'] = env['ccs_xl'] + env['ccs_yl']
env['mccs_yr'] = -env['ccs_yr']
env['mccs_yxr'] = -env['ccs_yr'] + (-env['ccs_xr'])
env['ccs_yxr'] = env['ccs_xr'] + env['ccs_yr']
env['fflr'] = env['ffl'] + (-env['ffr'])
ln_rfc = env.new_line(components=['rfc'])
env['ring_u'] = 8 * (28 * env['cell_u'] + ln_rfc)
env['arc_uu'] = 2 * env['cell_u']
env['arc_uv'] = 2 * env['cell_u'] + 2 * env['cell_v']
env['arc_ussu'] = (env['cell_us'] + env['straight_l']
                   + (-env['straight_r']) + (-env['cell_su']))
env['arc_ufrflu'] = (env['cell_uffl'] + env['ffl']
                  + (-env['ffr']) + (-env['cell_uffr']))
env['mffl'] = -env['ffl']
env['mffr'] = -env['ffr']
env['arc_us'] = (-env['straight_r'] + -env['cell_su'] + -env['cell_ur']
    + env['arc_octant'] + env['cell_ul'] + env['cell_us'] + env['straight_l'])
env['arc_sufl'] = (-env['straight_l'] + -env['cell_us'] + -env['cell_ul']
    + env['arc_octant'] + env['cell_l3'] + env['cell_uffl'] + env['ffl'])
env['arc_sufr'] = (-env['straight_r'] + -env['cell_su'] + -env['cell_ur']
    + env['arc_octant'] + env['cell_r3'] + env['cell_uffr'] + env['ffr'])
env['arc_sudsl'] = (-env['straight_l'] + -env['cell_us'] + -env['cell_ul']
    + env['arc_octant'] + env['cell_l3'] + env['cell_uffl'])
env['arc_sudsr'] = (-env['straight_r'] + -env['cell_su'] + -env['cell_ur']
    + env['arc_octant'] + env['cell_r3'] + env['cell_uffr'])
env['marc_sufl'] = -env['arc_sufl']
env['marc_sufr'] = -env['arc_sufr']
env['us_sector'] = env['arc_us'] + ln_rfc + env['arc_us']
env['fcc_sector_ds'] = (-env['arc_sudsr'] + ln_rfc + env['arc_sudsl'])
env['fcc_sector'] = (-env['arc_sufr'] + env['arc_sufl'])
env['fcc_sector_l'] = (-env['arc_sufl'] + ln_rfc + env['arc_sufl'])
env['fcc_sector_r'] = (-env['arc_sufr'] + ln_rfc + env['arc_sufr'])
env['ring_us'] = 4 * env['us_sector']
env['ring_us_ds'] = 4 * env['fcc_sector_ds']
env['ring_full'] = 4 * env['fcc_sector']