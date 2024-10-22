import xtrack as xt
env = xt.get_environment()
env.particle_ref = xt.Particles(mass0=xt.ELECTRON_MASS_EV, energy0=45.6e9)

env.new_line(name='cell_u', components=['qd1a', 'dr_01', 'dl1a', 'dr_01', 'qf2a', 'dr_01', 'sf2a', 'dr_01', 'dl2a', 'dr_01', 'sd1a', 'dr_01', 'qd3a', 'dr_01', 'dl2a', 'dr_01', 'sf1a', 'dr_01', 'qf4a', 'dr_01', 'dl2a', 'dr_01', 'sd2a', 'dr_01', 'qd5a', 'dr_01', 'dl3a', 'dr_01', 'qf6a', 'dr_01', 'dl3a', 'dr_01', 'qd5a', 'dr_01', 'sd2a', 'dr_01', 'dl2a', 'dr_01', 'qf4a', 'dr_01', 'sf1a', 'dr_01', 'dl2a', 'dr_01', 'qd3a', 'dr_01', 'sd1a', 'dr_01', 'dl2a', 'dr_01', 'sf2a', 'dr_01', 'qf2a', 'dr_01', 'dl1a', 'dr_01', 'qd1a'])
env.new_line(name='cell_v', components=['qd1a', 'dr_01', 'dl1a', 'dr_01', 'qf2a', 'dr_01', 'sf4a', 'dr_01', 'dl2a', 'dr_01', 'sd3a', 'dr_01', 'qd3a', 'dr_01', 'dl2a', 'dr_01', 'sf3a', 'dr_01', 'qf4a', 'dr_01', 'dl2a', 'dr_01', 'sd4a', 'dr_01', 'qd5a', 'dr_01', 'dl3a', 'dr_01', 'qf6a', 'dr_01', 'dl3a', 'dr_01', 'qd5a', 'dr_01', 'sd4a', 'dr_01', 'dl2a', 'dr_01', 'qf4a', 'dr_01', 'sf3a', 'dr_01', 'dl2a', 'dr_01', 'qd3a', 'dr_01', 'sd3a', 'dr_01', 'dl2a', 'dr_01', 'sf4a', 'dr_01', 'qf2a', 'dr_01', 'dl1a', 'dr_01', 'qd1a'])
env.new_line(name='cell_ul', components=['qd1a', 'dr_01', 'dl1a', 'dr_01', 'qf2a', 'dr_01', 'sf2a', 'dr_01', 'dl2a', 'dr_01', 'sd1a', 'dr_01', 'qd3a', 'dr_01', 'dl2a', 'dr_01', 'sf1a', 'dr_01', 'qf4a', 'dr_01', 'dl2a', 'dr_01', 'sd2a', 'dr_01', 'qd5a', 'dr_01', 'dl3a', 'dr_01', 'qf6a', 'dr_01', 'dl3a', 'dr_01', 'qd5a', 'dr_01', 'sd2aul', 'dr_01', 'dl2a', 'dr_01', 'qf4a', 'dr_01', 'sf1aul', 'dr_01', 'dl2a', 'dr_01', 'qd3a', 'dr_01', 'sd1aul', 'dr_01', 'dl2a', 'dr_01', 'sf2aul', 'dr_01', 'qf2a', 'dr_01', 'dl1a', 'dr_01', 'qd1a'])
env.new_line(name='cell_ur', components=['qd1a', 'dr_01', 'dl1a', 'dr_01', 'qf2a', 'dr_01', 'sf2a', 'dr_01', 'dl2a', 'dr_01', 'sd1a', 'dr_01', 'qd3a', 'dr_01', 'dl2a', 'dr_01', 'sf1a', 'dr_01', 'qf4a', 'dr_01', 'dl2a', 'dr_01', 'sd2a', 'dr_01', 'qd5a', 'dr_01', 'dl3a', 'dr_01', 'qf6a', 'dr_01', 'dl3a', 'dr_01', 'qd5a', 'dr_01', 'sd2aur', 'dr_01', 'dl2a', 'dr_01', 'qf4a', 'dr_01', 'sf1aur', 'dr_01', 'dl2a', 'dr_01', 'qd3a', 'dr_01', 'sd1aur', 'dr_01', 'dl2a', 'dr_01', 'sf2aur', 'dr_01', 'qf2a', 'dr_01', 'dl1a', 'dr_01', 'qd1a'])
env.new_line(name='cell_l2', components=['qd1a', 'dr_01', 'dl1a', 'dr_01', 'qf2a', 'dr_01', 'sf2al2', 'dr_01', 'dl2a', 'dr_01', 'sd1al2', 'dr_01', 'qd3a', 'dr_01', 'dl2a', 'dr_01', 'sf1al2', 'dr_01', 'qf4a', 'dr_01', 'dl2a', 'dr_01', 'sd2al2', 'dr_01', 'qd5a', 'dr_01', 'dl3a', 'dr_01', 'qf6a', 'dr_01', 'dl3a', 'dr_01', 'qd5a', 'dr_01', 'sd2bl2', 'dr_01', 'dl2a', 'dr_01', 'qf4a', 'dr_01', 'sf1bl2', 'dr_01', 'dl2a', 'dr_01', 'qd3a', 'dr_01', 'sd1bl2', 'dr_01', 'dl2a', 'dr_01', 'sf2bl2', 'dr_01', 'qf2a', 'dr_01', 'dl1a', 'dr_01', 'qd1a'])
env.new_line(name='cell_l3', components=['qd1a', 'dr_01', 'dl1a', 'dr_01', 'qf2a', 'dr_01', 'sf2al3', 'dr_01', 'dl2a', 'dr_01', 'sd1al3', 'dr_01', 'qd3a', 'dr_01', 'dl2a', 'dr_01', 'sf1al3', 'dr_01', 'qf4a', 'dr_01', 'dl2a', 'dr_01', 'sd2al3', 'dr_01', 'qd5a', 'dr_01', 'dl3a', 'dr_01', 'qf6a', 'dr_01', 'dl3a', 'dr_01', 'qd5a', 'dr_01', 'sd2bl3', 'dr_01', 'dl2a', 'dr_01', 'qf4a', 'dr_01', 'sf1bl3', 'dr_01', 'dl2a', 'dr_01', 'qd3a', 'dr_01', 'sd1bl3', 'dr_01', 'dl2a', 'dr_01', 'sf2bl3', 'dr_01', 'qf2a', 'dr_01', 'dl1a', 'dr_01', 'qd1a'])
env.new_line(name='cell_r2', components=['qd1a', 'dr_01', 'dl1a', 'dr_01', 'qf2a', 'dr_01', 'sf2ar2', 'dr_01', 'dl2a', 'dr_01', 'sd1ar2', 'dr_01', 'qd3a', 'dr_01', 'dl2a', 'dr_01', 'sf1ar2', 'dr_01', 'qf4a', 'dr_01', 'dl2a', 'dr_01', 'sd2ar2', 'dr_01', 'qd5a', 'dr_01', 'dl3a', 'dr_01', 'qf6a', 'dr_01', 'dl3a', 'dr_01', 'qd5a', 'dr_01', 'sd2br2', 'dr_01', 'dl2a', 'dr_01', 'qf4a', 'dr_01', 'sf1br2', 'dr_01', 'dl2a', 'dr_01', 'qd3a', 'dr_01', 'sd1br2', 'dr_01', 'dl2a', 'dr_01', 'sf2br2', 'dr_01', 'qf2a', 'dr_01', 'dl1a', 'dr_01', 'qd1a'])
env.new_line(name='cell_r3', components=['qd1a', 'dr_01', 'dl1a', 'dr_01', 'qf2a', 'dr_01', 'sf2ar3', 'dr_01', 'dl2a', 'dr_01', 'sd1ar3', 'dr_01', 'qd3a', 'dr_01', 'dl2a', 'dr_01', 'sf1ar3', 'dr_01', 'qf4a', 'dr_01', 'dl2a', 'dr_01', 'sd2ar3', 'dr_01', 'qd5a', 'dr_01', 'dl3a', 'dr_01', 'qf6a', 'dr_01', 'dl3a', 'dr_01', 'qd5a', 'dr_01', 'sd2br3', 'dr_01', 'dl2a', 'dr_01', 'qf4a', 'dr_01', 'sf1br3', 'dr_01', 'dl2a', 'dr_01', 'qd3a', 'dr_01', 'sd1br3', 'dr_01', 'dl2a', 'dr_01', 'sf2br3', 'dr_01', 'qf2a', 'dr_01', 'dl1a', 'dr_01', 'qd1a'])
env.new_line(name='cell_us', components=['qd1a', 'dr_01', 'dl1a', 'dr_01', 'qfs0a', 'dr_01', 'sf2asl', 'dr_01', 'dl2a', 'dr_01', 'sd1asl', 'dr_01', 'qds0a', 'dr_01', 'dl2a', 'dr_01', 'sf1asl', 'dr_01', 'qfs1a', 'dr_01', 'ds_01', 'ds1a', 'ds_01', 'dr_01', 'sd2asl', 'dr_01', 'qds2a', 'dr_01', 'ds_02', 'ds2a', 'ds_02', 'dr_01', 'qfs3a', 'dr_01', 'ds_03', 'ds3a', 'ds_03', 'dr_01', 'qds4a', 'dr_01', 'ds_04', 'ds4a', 'ds_04', 'dr_01', 'qfs5a', 'dr_01', 'sf3asl'])
env.new_line(name='cell_su', components=['qd1a', 'dr_01', 'dl1a', 'dr_01', 'qfs0a', 'dr_01', 'sf2asr', 'dr_01', 'dl2a', 'dr_01', 'sd1asr', 'dr_01', 'qds0a', 'dr_01', 'dl2a', 'dr_01', 'sf1asr', 'dr_01', 'qfs1a', 'dr_01', 'ds_01', 'ds1a', 'ds_01', 'dr_01', 'sd2asr', 'dr_01', 'qds2a', 'dr_01', 'ds_02', 'ds2a', 'ds_02', 'dr_01', 'qfs3a', 'dr_01', 'ds_03', 'ds3a', 'ds_03', 'dr_01', 'qds4a', 'dr_01', 'ds_04', 'ds4a', 'ds_04', 'dr_01', 'qfs5a', 'dr_01', 'sf3asr'])
env.new_line(name='cell_uffl', components=['qd1a', 'dr_01', 'dl1a', 'dr_01', 'qfm0l', 'dr_01', 'sf2afl', 'dr_01', 'dl2a', 'dr_01', 'sd1afl', 'dr_01', 'qdm0l', 'dr_01', 'dl2a', 'dr_01', 'sf1afl', 'dr_01', 'qfm1l', 'dr_01', 'df2a', 'dr_01', 'sd2afl', 'dr_01', 'qdm2l', 'dr_01', 'df3a', 'dr_01', 'qfm3l', 'dr_01', 'sf3afl', 'dr_01', 'df3a', 'dr_01', 'qdm4l', 'dr_01', 'df2a', 'dr_01', 'qfm5l', 'dl_02a', 'qdm6l', 'dl_02b', 'qfm7l', 'dl_02c', 'qdm8l', 'dr_01', 2*['scrabl']])
env.new_line(name='cell_uffr', components=['qd1a', 'dr_01', 'dl1a', 'dr_01', 'qfm0r', 'dr_01', 'sf2afr', 'dr_01', 'dl2a', 'dr_01', 'sd1afr', 'dr_01', 'qdm0r', 'dr_01', 'dl2a', 'dr_01', 'sf1afr', 'dr_01', 'qfm1r', 'dr_01', 'df2a', 'dr_01', 'sd2afr', 'dr_01', 'qdm2r', 'dr_01', 'df3a', 'dr_01', 'qfm3r', 'dr_01', 'sf3afr', 'dr_01', 'df3a', 'dr_01', 'qdm4r', 'dr_01', 'df2a', 'dr_01', 'qfm5r', 'dl_02a', 'qdm6r', 'dl_02b', 'qfm7r', 'dl_02c', 'qdm8r', 'dr_01', 2*['scrabr']])
env.new_line(name='straight_l', components=['dl_00', 'qdl1a', 'dl_04', 'qfl2a', 'dl_01', 'qdl2a', 'dl_01', 'qfl3a', 'dl_01m', 'rfc', 'dl_01m', 'qdl3a', 'dl_01', 'qfl6a', 'dl_01', 'qdl4a', 'dl_06', 'ds1l', 'dl_05', 'qfl4a', 'dl_01', 'qdl5a', 'dl_01', 'qfl5a', 'dl_01', 'qdl5a', 'dl_01', 'qfl5a', 'dl_01', 'qdl6a', 'scenter'])
env.new_line(name='straight_r', components=['dl_00', 'qdl1a', 'dl_04', 'qfl2a', 'dl_01', 'qdl2a', 'dl_01', 'qfl3a', 'dl_01', 'qdl3a', 'dl_01', 'qfl6a', 'dl_01', 'qdl4a', 'dl_06', 'ds1r', 'dl_05', 'qfl4a', 'dl_01', 'qdl5a', 'dl_01', 'qfl5a', 'dl_01', 'qdl5a', 'dl_01', 'qfl5a', 'dl_01', 'qdl6a', 'scenter'])
env.new_line(name='ccs_xl', components=[2*['scrabl'], 'lx0', 'qd20l', 'd8l', 'qf19l', 'd8l', 'qd18l', 'd8l', 'qf17l', 'd8l', 'qd16l', 'lx0', 'b7l', 'lx0', 'qf15l', 'lx0', 'b7l', 'lx0', 'qd14l', 'd7l', 'qf13l', 'lx0', 'decfl', 4*['sfx2l'], 'lx0', 'qx0l', 'd7l', 'qx1l', 'lx0', 'b6l', 'lx0', 'qx2l', 'ipimag4', 'qx2l', 'lx0', 'b6l', 'lx0', 'qx1l', 'd7l', 'qx0l', 'lx0', 4*['sfx1l'], 'decfl', 'lx0', 'qf12l', 'd7l', 'qd11l', 'lx0', 'b5l', 'lx0', 'oct2l', 2*['sfm2l'], 'lx0'])
env.new_line(name='ccs_yl', components=['ipimag3', 'qf10l', 'lx0', 'b4lc', 'lx0', 'qd9l', 'lx0', 'b4lb', 'lx0', 'qf8l', 'lx0', 'b4la', 'lx0', 'qd7l', 'lx0', 4*['sdy2l'], 'decdl', 'lx0', 'qy1l', 'd3l', 'qy2l', 'd3l', 'qy3l', 'd4l', 'qy3l', 'lx0', 'b3l', 'lx0', 'qy4l', 'ipimag2', 'qy4l', 'lx0', 'b3l', 'lx0', 'qy3l', 'd4l', 'qy3l', 'd3l', 'qy2l', 'd3l', 'qy1l', 'lx0', 4*['sdy1l'], 'decdl', 'lx0', 'qd6l', 'lx0', 'b1lb', 'lx0', 'qf5l', 'lx0', 'b1la', 'lx0', 'qd4l', 'lx0', 2*['sdm1l'], 'oct1l', 'dec1l', 'lx0', 'b0l', 'lx0', 'qd2l', 'lx0', 'b0l', 'lx0', 'qf2l', 'lx0', 'bsl', 'lx0', 'qd1l', 'd2', 'oct0l', 'qf1bl', 'lx0', 'qf1al', 'd1', 'qd0bl', 'lx0', 'qd0al', 'd0', 'ip'])
env.new_line(name='ccs_xr', components=[2*['scrabr'], 'lx0', 'qd20r', 'd8r', 'qf19r', 'd8r', 'qd18r', 'd8r', 'qf17r', 'd8r', 'qd16r', 'lx0', 'b7r', 'lx0', 'qf15r', 'lx0', 'b7r', 'lx0', 'qd14r', 'd7r', 'qf13r', 'lx0', 'decfr', 4*['sfx2r'], 'lx0', 'qx0r', 'd7r', 'qx1r', 'lx0', 'b6r', 'lx0', 'qx2r', 'ipimag4', 'qx2r', 'lx0', 'b6r', 'lx0', 'qx1r', 'd7r', 'qx0r', 'lx0', 4*['sfx1r'], 'decfr', 'lx0', 'qf12r', 'd7r', 'qd11r', 'lx0', 'b5rb', 'lx0', 'oct2r', 2*['sfm2r'], 'lx0'])
env.new_line(name='ccs_yr', components=['ipimag3', 'qf10r', 'lx0', 'b5ra', 'lx0', 'qd9r', 'lx0', 'b4rb', 'lx0', 'qf8r', 'lx0', 'b4ra', 'lx0', 'qd7r', 'lx0', 4*['sdy2r'], 'decdr', 'lx0', 'qy1r', 'lx0', 'b3r', 'lx0', 'qy2r', 'lx0', 'b3r', 'lx0', 'qy3r', 'lx0', 'b3r', 'lx0', 'qy4r', 'ipimag2', 'qy4r', 'lx0', 'b3r', 'lx0', 'qy3r', 'lx0', 'b3r', 'lx0', 'qy2r', 'lx0', 'b3r', 'lx0', 'qy1r', 'lx0', 4*['sdy1r'], 'decdr', 'lx0', 'qd6r', 'lx0', 'b1rb', 'lx0', 'qf5r', 'lx0', 'b1ra', 'lx0', 'qd4r', 'lx0', 2*['sdm1r'], 'oct1r', 'dec1r', 'lx0', 'b0r', 'lx0', 'qd2r', 'lx0', 'bsr', 'lx0', 'qf2r', 'lx0', 'bsr', 'lx0', 'qd1r', 'd2r', 'oct0r', 'qf1br', 'lx0', 'qf1ar', 'd1', 'qd0br', 'lx0', 'qd0ar', 'd0', 'ip'])

# Name convention:

# - cell_u: arc cell
# - cell_ul: same as cell_u with different sextupoles
# - cell_ur: same as cell_u with different sextupoles
# - cell_l3: same as cell_u with different sextupoles
# - cell_r3: same as cell_u with different sextupoles

# - cell_us: short curved cell on the left side of the service straight (dedicated quads)
# - cell_su: short curved cell on the right side of the service straight (dedicated quads)
# - cell_uffl: curved cell on the left side of the experimental insertion (dedicated quads)
# - cell_uffr: curved cell on the right side of the experimental insertion (dedicated quads)

# - ccs_yl: ip + triplet + vertical chromatic correction section for left side
# - ccs_yr: ip + triplet + vertical chromatic correction section for right side
# - ccs_xl: horizontal chromatic correction section for left side
# - ccs_xr: horizontal chromatic correction section for right side

# - straight_l: left side of the service straight
# - straight_r: right side of the service straight

# Note that l/r are for the service insertion are defined wrt the ip and not
# wrt the center of the insertion

# New ring definition (line called `fccee_p_ring`)

env['arc_octant'] = 25 * env['cell_u']

env['ffl'] = env['ccs_xl'] + env['ccs_yl']
env['ffr'] = env['ccs_xr'] + env['ccs_yr']
env['experimental_insertion_l'] =  (env['cell_l3'] + env['cell_uffl'] + env['ffl'])
env['experimental_insertion_r'] = -(env['cell_r3'] + env['cell_uffr'] + env['ffr'])

env['service_insertion_l'] = -(env['cell_ul'] + env['cell_us'] + env['straight_l'])
env['service_insertion_r'] =  (env['cell_ur'] + env['cell_su'] + env['straight_r'])

env['fcc_quarter'] = (env['experimental_insertion_r']
                    + env['arc_octant']
                    + env['service_insertion_r']
                    + env['service_insertion_l']
                    + env['arc_octant']
                    + env['experimental_insertion_l'])

env['fccee_p_ring'] = 4 * env['fcc_quarter']

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

# Check that the two rings are the same
# for nn1, nn2, in zip(env['ring_full'].get_table().name[:],
#                      env['fccee_p_ring'].get_table().name[:]):
#     if nn1 != nn2:
#         print(nn1, nn2)