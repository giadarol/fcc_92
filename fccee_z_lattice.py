####################
# FCC-ee z lattice #
####################

# Name convention:

# - cell_u: arc cell
# - cell_ul: same as cell_u with different sextupoles, used on the left of the service straight
# - cell_ur: same as cell_u with different sextupoles, used on the right of the service straight
# - cell_l3: same as cell_u with different sextupoles, used on the left of the experimental insertion
# - cell_r3: same as cell_u with different sextupoles, used on the right of the experimental insertion

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
# wrt the center of the insertion.

import xtrack as xt
env = xt.get_environment()
env.vars.default_to_zero=True

# Lattice parameters:
env["adf1"] = 0.4
env["ads1"] = 0.56
env["ads2"] = 0.56
env["ads3"] = 0.554
env["ang0"] = "((((6.2831853 - (4.0 * fflr_angle)) / 224.0) / 10.0) / ang_rescaling_ds)"
env["ang_rescaling_ds"] = "(1.0 + ((((32.0 * adf1) * bxyff) / 224.0) / 10.0))"
env["angffl"] = "(angtfl / ((((((((((((1.0 * b0fl) * 0.76) + ((2.0 * b0fl) * 1.1)) + ((1.0 * b0fl) * 1.38)) + ((1.0 * b1fl) * 1.68)) + ((2.0 * b3fl) * 0.71)) + ((1.0 * b4fl) * 1.37)) + ((1.0 * b4fl) * 0.98)) + ((1.0 * b4fl) * 0.98)) + ((1.0 * b5fl) * 0.8)) + ((2.0 * b6fl) * 0.72)) + ((2.0 * b7fl) * 0.72)))"
env["angffr"] = "(angtfr / ((((((((((2.0 * b0fr) * 0.451) + ((1.0 * b0fr) * 0.451)) + ((1.0 * b1fr) * 0.546)) + ((1.0 * b1fr) * 0.666)) + ((6.0 * b3fr) * 0.665)) + ((2.0 * b4fr) * 0.76)) + ((2.0 * b5fr) * 0.84)) + ((2.0 * b6fr) * 0.84)) + ((2.0 * b7fr) * 0.84)))"
env["angs1l"] = "(-0.0006251 * dogleg_on)"
env["angtfl"] = "(((fflr_angle * 0.5) - (theta_cross * 0.5)) - dang0)"
env["angtfr"] = "(((fflr_angle * 0.5) + (theta_cross * 0.5)) + dang0)"
env["b0fl"] = 0.3068
env["b0fr"] = 1.0
env["b1fl"] = 0.9467407
env["b1fr"] = "b0fr"
env["b3fl"] = 2.02
env["b3fr"] = 1.0
env["b4fl"] = 0.7761993
env["b4fr"] = 0.4177369
env["b5fl"] = 3.622775
env["b5fr"] = 1.222555
env["b6fl"] = 3.7217
env["b6fr"] = 1.4881
env["b7fl"] = 3.146938
env["b7fr"] = 0.8658736
env["bxfr"] = 0.03695179
env["bxyff"] = "((1.0 + (bxfr / 3.0)) - (byfr / 6.0))"
env["byfr"] = -0.003034615
env["clength_adj"] = 1.467
env["dang0"] = 0.0
env["dd56"] = -0.004801018
env["dl_len"] = 28.94695
env["dogleg_on"] = 0.0
env["fflr_angle"] = 0.107
env["l_sxtd"] = 0.6
env["l_sxtf"] = 0.6
env["l_sxtm"] = 0.6
env["lbfl"] = 55.88
env["lbfr"] = 61.95
env["ldsxt"] = 0.52
env["len_qd1"] = 0.96
env["len_qd3"] = 1.86
env["len_qd5"] = 1.83
env["len_qf2"] = 2.39
env["len_qf4"] = 2.4
env["len_qf6"] = 2.37
env["lfsxt"] = 0.3
env["lq2"] = 1.6
env["lq3"] = 0.8
env["lq4"] = 2.4
env["rf_lag"] = 0.4
env["rf_on"] = 1.0
env["rf_voltage"] = "(50.0 * rf_on)"
env["theta_cross"] = 0.03

# Base types
env.new("sbend", "Bend")
env.new("rbend", "Bend", rbend=True)
env.new("quadrupole", "Quadrupole")
env.new("sextupole", "Sextupole")
env.new("octupole", "Octupole")
env.new("marker", "Marker")
env.new("rfcavity", "Cavity")
env.new("multipole", "Multipole", knl=[0, 0, 0, 0, 0, 0])
env.new("solenoid", "Solenoid")
env.new("drift", "Drift")

# marker elements:
env.new('cellcenter', 'marker')
env.new('scenter', 'marker')
env.new('ipimag1', 'marker')
env.new('ipimag2', 'marker')
env.new('ipimag3', 'marker')
env.new('ipimag4', 'marker')
env.new('ipimag5', 'marker')
env.new('begff', 'marker')
env.new('ip', 'marker')

# sbend elements:
env.new('dl1a', 'sbend', length='(dl_len * (1.0 + byfr))', angle='(ang0 * (1.0 + byfr))', extra={}, rbend=False, rbarc=True, k0_from_h=True)
env.new('dl2a', 'sbend', length='(dl_len * ((1.0 - (byfr / 3.0)) - (bxfr / 3.0)))', angle='(ang0 * ((1.0 - (byfr / 3.0)) - (bxfr / 3.0)))', extra={}, rbend=False, rbarc=True, k0_from_h=True)
env.new('dl3a', 'sbend', length='(dl_len * (1.0 + bxfr))', angle='(ang0 * (1.0 + bxfr))', extra={}, rbend=False, rbarc=True, k0_from_h=True)
env.new('df2a', 'sbend', length='((dl_len * ((1.0 - (byfr / 3.0)) - (bxfr / 3.0))) * (0.5 + adf1))', angle='((ang0 * ((1.0 - (byfr / 3.0)) - (bxfr / 3.0))) * (0.5 + adf1))', extra={}, rbend=False, rbarc=True, k0_from_h=True)
env.new('df3a', 'sbend', length='((dl_len * (1.0 + bxfr)) * (0.5 + adf1))', angle='((ang0 * (1.0 + bxfr)) * (0.5 + adf1))', extra={}, rbend=False, rbarc=True, k0_from_h=True)
env.new('ds1a', 'sbend', length='((dl_len * bxyff) * ads1)', angle='((ang0 * bxyff) * ads1)', extra={}, rbend=False, rbarc=True, k0_from_h=True)
env.new('ds2a', 'sbend', length='((dl_len * bxyff) * ads2)', angle='((ang0 * bxyff) * ads2)', extra={}, rbend=False, rbarc=True, k0_from_h=True)
env.new('ds3a', 'sbend', length='((dl_len * bxyff) * ads3)', angle='((ang0 * bxyff) * ads3)', extra={}, rbend=False, rbarc=True, k0_from_h=True)
env.new('ds4a', 'sbend', length='((dl_len * bxyff) * (((2.0 - ads1) - ads2) - ads3))', angle='((ang0 * bxyff) * (((2.0 - ads1) - ads2) - ads3))', extra={}, rbend=False, rbarc=True, k0_from_h=True)
env.new('ds1l', 'sbend', length=7.9, angle='angs1l', extra={}, rbend=False, rbarc=True, k0_from_h=True)
env.new('ds1r', 'sbend', length=7.9, angle='-angs1l', extra={}, rbend=False, rbarc=True, k0_from_h=True)

# rbend elements:
env.new('b7l', 'rbend', length='(lbfl * 0.72)', angle='((angffl * b7fl) * 0.72)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('b6l', 'rbend', length='(lbfl * 0.72)', angle='((angffl * b6fl) * 0.72)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('b5l', 'rbend', length='(lbfl * 0.8)', angle='((angffl * b5fl) * 0.8)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('b4lc', 'rbend', length='(lbfl * 0.98)', angle='((angffl * b4fl) * 0.98)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('b4lb', 'rbend', length='(lbfl * 0.98)', angle='((angffl * b4fl) * 0.98)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('b4la', 'rbend', length='(lbfl * 1.16)', angle='((angffl * b4fl) * 1.37)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('b3l', 'rbend', length='(lbfl * 0.71)', angle='((angffl * b3fl) * 0.71)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('b1lb', 'rbend', length='(lbfl * 1.68)', angle='((angffl * b1fl) * 1.68)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('b1la', 'rbend', length='(lbfl * 1.38)', angle='((angffl * b0fl) * 1.38)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('b0l', 'rbend', length='(lbfl * 1.1)', angle='((angffl * b0fl) * 1.1)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('bsl', 'rbend', length='(lbfl * 0.76)', angle='((angffl * b0fl) * 0.76)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('b7r', 'rbend', length='(lbfr * 0.84)', angle='((angffr * b7fr) * 0.84)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('b6r', 'rbend', length='(lbfr * 0.84)', angle='((angffr * b6fr) * 0.84)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('b5rb', 'rbend', length='(lbfr * 0.84)', angle='((angffr * b5fr) * 0.94)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('b5ra', 'rbend', length='(lbfr * 0.84)', angle='((angffr * b5fr) * 0.74)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('b4rb', 'rbend', length='(lbfr * 0.76)', angle='((angffr * b4fr) * 0.66)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('b4ra', 'rbend', length='(lbfr * 0.76)', angle='((angffr * b4fr) * 0.86)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('b3r', 'rbend', length='(lbfr * 0.665)', angle='((angffr * b3fr) * 0.665)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('b1rb', 'rbend', length='(lbfr * 0.749)', angle='((angffr * b1fr) * 0.749)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('b1ra', 'rbend', length='(lbfr * 0.547)', angle='((angffr * b1fr) * 0.547)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('b0r', 'rbend', length='(lbfr * 0.358)', angle='((angffr * b0fr) * 0.423)', extra={}, rbend=True, rbarc=True, k0_from_h=True)
env.new('bsr', 'rbend', length='(lbfr * 0.358)', angle='((angffr * b0fr) * 0.423)', extra={}, rbend=True, rbarc=True, k0_from_h=True)

# quadrupole elements:
env.new('qd1a', 'quadrupole', length='len_qd1', k1='kqd1')
env.new('qf2a', 'quadrupole', length='len_qf2', k1='kqf2')
env.new('qd3a', 'quadrupole', length='len_qd3', k1='kqd3')
env.new('qf4a', 'quadrupole', length='len_qf4', k1='kqf4')
env.new('qd5a', 'quadrupole', length='len_qd5', k1='kqd5')
env.new('qf6a', 'quadrupole', length='len_qf6', k1='kqf6')
env.new('qfs0a', 'quadrupole', length='len_qf2', k1='kqfs0')
env.new('qds0a', 'quadrupole', length='len_qd3', k1='kqds0')
env.new('qfs1a', 'quadrupole', length='len_qf4', k1='kqfs1')
env.new('qds2a', 'quadrupole', length='len_qd5', k1='kqds2')
env.new('qfs3a', 'quadrupole', length='len_qf6', k1='kqfs3')
env.new('qds4a', 'quadrupole', length='len_qd5', k1='kqds4')
env.new('qfs5a', 'quadrupole', length='len_qf4', k1='kqfs5')
env.new('qfl1a', 'quadrupole', length=1.0, k1='kqfl1')
env.new('qdl1a', 'quadrupole', length=1.0, k1='kqdl1')
env.new('qfl2a', 'quadrupole', length=1.0, k1='kqfl2')
env.new('qdl2a', 'quadrupole', length=1.0, k1='kqdl2')
env.new('qfl3a', 'quadrupole', length=1.0, k1='kqfl3')
env.new('qdl3a', 'quadrupole', length=1.0, k1='kqdl3')
env.new('qfl4a', 'quadrupole', length=1.0, k1='kqfl4')
env.new('qdl4a', 'quadrupole', length=1.0, k1='kqdl4')
env.new('qfl5a', 'quadrupole', length=1.0, k1='kqfl5')
env.new('qdl5a', 'quadrupole', length=1.0, k1='kqdl5')
env.new('qfl6a', 'quadrupole', length=1.0, k1='kqfl6')
env.new('qdl6a', 'quadrupole', length=0.5, k1='kqdl6')
env.new('qfm0l', 'quadrupole', length='len_qf2', k1='kqfm0l')
env.new('qdm0l', 'quadrupole', length='len_qd3', k1='kqdm0l')
env.new('qfm1l', 'quadrupole', length='len_qf4', k1='kqfm1l')
env.new('qdm2l', 'quadrupole', length='len_qd5', k1='kqdm2l')
env.new('qfm3l', 'quadrupole', length='len_qf6', k1='kqfm3l')
env.new('qdm4l', 'quadrupole', length='len_qd5', k1='kqdm4l')
env.new('qfm5l', 'quadrupole', length='len_qf4', k1='kqfm5l')
env.new('qdm6l', 'quadrupole', length='len_qd5', k1='kqdm6l')
env.new('qfm7l', 'quadrupole', length='len_qd5', k1='kqfm7l')
env.new('qdm8l', 'quadrupole', length='len_qd5', k1='kqdm8l')
env.new('qfm0r', 'quadrupole', length='len_qf2', k1='kqfm0r')
env.new('qdm0r', 'quadrupole', length='len_qd3', k1='kqdm0r')
env.new('qfm1r', 'quadrupole', length='len_qf4', k1='kqfm1r')
env.new('qdm2r', 'quadrupole', length='len_qd5', k1='kqdm2r')
env.new('qfm3r', 'quadrupole', length='len_qf6', k1='kqfm3r')
env.new('qdm4r', 'quadrupole', length='len_qd5', k1='kqdm4r')
env.new('qfm5r', 'quadrupole', length='len_qf4', k1='kqfm5r')
env.new('qdm6r', 'quadrupole', length='len_qd5', k1='kqdm6r')
env.new('qfm7r', 'quadrupole', length='len_qd5', k1='kqfm7r')
env.new('qdm8r', 'quadrupole', length='len_qd5', k1='kqdm8r')
env.new('qx2l', 'quadrupole', length='(lq2 / 2.0)', k1='kqx02l')
env.new('qx1l', 'quadrupole', length='lq2', k1='kqx01l')
env.new('qx0l', 'quadrupole', length='lq3', k1='kqx00l')
env.new('qy4l', 'quadrupole', length='(lq2 / 2.0)', k1='kqy04l')
env.new('qy3l', 'quadrupole', length='lq3', k1='kqy03l')
env.new('qy2l', 'quadrupole', length='lq2', k1='kqy02l')
env.new('qy1l', 'quadrupole', length='lq3', k1='kqy01l')
env.new('qd20l', 'quadrupole', length='lq2', k1='kqd20l')
env.new('qf19l', 'quadrupole', length='lq4', k1='kqf19l')
env.new('qd18l', 'quadrupole', length='lq4', k1='kqd18l')
env.new('qf17l', 'quadrupole', length='lq4', k1='kqf17l')
env.new('qd16l', 'quadrupole', length='lq2', k1='kqd16l')
env.new('qf15l', 'quadrupole', length='lq4', k1='kqf15l')
env.new('qd14l', 'quadrupole', length='lq2', k1='kqd14l')
env.new('qf13l', 'quadrupole', length='lq3', k1='kqf13l')
env.new('qf12l', 'quadrupole', length='lq3', k1='kqf12l')
env.new('qd11l', 'quadrupole', length='lq2', k1='kqd11l')
env.new('qf10l', 'quadrupole', length='lq2', k1='kqf10l')
env.new('qd9l', 'quadrupole', length='lq3', k1='kqd09l')
env.new('qf8l', 'quadrupole', length='lq2', k1='kqf08l')
env.new('qd7l', 'quadrupole', length='lq3', k1='kqd07l')
env.new('qd6l', 'quadrupole', length='lq3', k1='kqd06l')
env.new('qf5l', 'quadrupole', length='lq2', k1='kqf05l')
env.new('qd4l', 'quadrupole', length='lq3', k1='kqd04l')
env.new('qd2l', 'quadrupole', length='lq3', k1='kqd02l')
env.new('qf2l', 'quadrupole', length='lq3', k1='kqf02l')
env.new('qd1l', 'quadrupole', length='lq3', k1='kqd01l')
env.new('qf1bl', 'quadrupole', length=1.5, k1='kqf1bl')
env.new('qf1al', 'quadrupole', length=1.5, k1='kqf1al')
env.new('qd0bl', 'quadrupole', length=1.75, k1='kqd0bl')
env.new('qd0al', 'quadrupole', length=1.75, k1='kqd0al')
env.new('qx2r', 'quadrupole', length='(lq2 / 2.0)', k1='kqx02r')
env.new('qx1r', 'quadrupole', length='lq2', k1='kqx01r')
env.new('qx0r', 'quadrupole', length='lq3', k1='kqx00r')
env.new('qy4r', 'quadrupole', length='(lq2 / 2.0)', k1='kqy04r')
env.new('qy3r', 'quadrupole', length='lq2', k1='kqy03r')
env.new('qy2r', 'quadrupole', length='lq2', k1='kqy02r')
env.new('qy1r', 'quadrupole', length='lq2', k1='kqy01r')
env.new('qd20r', 'quadrupole', length='lq3', k1='kqd20r')
env.new('qf19r', 'quadrupole', length='lq2', k1='kqf19r')
env.new('qd18r', 'quadrupole', length='lq2', k1='kqd18r')
env.new('qf17r', 'quadrupole', length='lq2', k1='kqf17r')
env.new('qd16r', 'quadrupole', length='lq2', k1='kqd16r')
env.new('qf15r', 'quadrupole', length='lq2', k1='kqf15r')
env.new('qd14r', 'quadrupole', length='lq2', k1='kqd14r')
env.new('qf13r', 'quadrupole', length='lq3', k1='kqf13r')
env.new('qf12r', 'quadrupole', length='lq3', k1='kqf12r')
env.new('qd11r', 'quadrupole', length='lq2', k1='kqd11r')
env.new('qf10r', 'quadrupole', length='lq2', k1='kqf10r')
env.new('qd9r', 'quadrupole', length='lq3', k1='kqd09r')
env.new('qf8r', 'quadrupole', length='lq2', k1='kqf08r')
env.new('qd7r', 'quadrupole', length='lq2', k1='kqd07r')
env.new('qd6r', 'quadrupole', length='lq2', k1='kqd06r')
env.new('qf5r', 'quadrupole', length='lq2', k1='kqf05r')
env.new('qd4r', 'quadrupole', length='lq2', k1='kqd04r')
env.new('qd2r', 'quadrupole', length='lq3', k1='kqd02r')
env.new('qf2r', 'quadrupole', length='lq3', k1='kqf02r')
env.new('qd1r', 'quadrupole', length='lq3', k1='kqd01r')
env.new('qf1br', 'quadrupole', length=1.5, k1='kqf1br')
env.new('qf1ar', 'quadrupole', length=1.5, k1='kqf1ar')
env.new('qd0br', 'quadrupole', length=1.75, k1='kqd0br')
env.new('qd0ar', 'quadrupole', length=1.75, k1='kqd0ar')

# sextupole elements:
env.new('sf1a', 'sextupole', length='lfsxt', k2='ksf1')
env.new('sf2a', 'sextupole', length='lfsxt', k2='ksf2')
env.new('sd1a', 'sextupole', length='ldsxt', k2='ksd1')
env.new('sd2a', 'sextupole', length='ldsxt', k2='ksd2')
env.new('sf3a', 'sextupole', length='lfsxt', k2='ksf3')
env.new('sf4a', 'sextupole', length='lfsxt', k2='ksf4')
env.new('sd3a', 'sextupole', length='ldsxt', k2='ksd3')
env.new('sd4a', 'sextupole', length='ldsxt', k2='ksd4')
env.new('sf1aul', 'sextupole', length='lfsxt', k2='ksf1ul')
env.new('sf2aul', 'sextupole', length='lfsxt', k2='ksf2ul')
env.new('sf1aur', 'sextupole', length='lfsxt', k2='ksf1ur')
env.new('sf2aur', 'sextupole', length='lfsxt', k2='ksf2ur')
env.new('sd1aul', 'sextupole', length='ldsxt', k2='ksd1ul')
env.new('sd2aul', 'sextupole', length='ldsxt', k2='ksd2ul')
env.new('sd1aur', 'sextupole', length='ldsxt', k2='ksd1ur')
env.new('sd2aur', 'sextupole', length='ldsxt', k2='ksd2ur')
env.new('sf1asl', 'sextupole', length='lfsxt', k2='ksf1sl')
env.new('sf2asl', 'sextupole', length='lfsxt', k2='ksf2sl')
env.new('sf1asr', 'sextupole', length='lfsxt', k2='ksf1sr')
env.new('sf2asr', 'sextupole', length='lfsxt', k2='ksf2sr')
env.new('sf3asl', 'sextupole', length='lfsxt', k2='ksf3sl')
env.new('sf3asr', 'sextupole', length='lfsxt', k2='ksf3sr')
env.new('sd1asl', 'sextupole', length='ldsxt', k2='ksd1sl')
env.new('sd2asl', 'sextupole', length='ldsxt', k2='ksd2sl')
env.new('sd1asr', 'sextupole', length='ldsxt', k2='ksd1sr')
env.new('sd2asr', 'sextupole', length='ldsxt', k2='ksd2sr')
env.new('sf1afl', 'sextupole', length='lfsxt', k2='ksf1fl')
env.new('sf2afl', 'sextupole', length='lfsxt', k2='ksf2fl')
env.new('sf1afr', 'sextupole', length='lfsxt', k2='ksf1fr')
env.new('sf2afr', 'sextupole', length='lfsxt', k2='ksf2fr')
env.new('sf3afl', 'sextupole', length='lfsxt', k2='ksf3fl')
env.new('sf3afr', 'sextupole', length='lfsxt', k2='ksf3fr')
env.new('sd1afl', 'sextupole', length='ldsxt', k2='ksd1fl')
env.new('sd2afl', 'sextupole', length='ldsxt', k2='ksd2fl')
env.new('sd1afr', 'sextupole', length='ldsxt', k2='ksd1fr')
env.new('sd2afr', 'sextupole', length='ldsxt', k2='ksd2fr')
env.new('sf1al2', 'sextupole', length='lfsxt', k2='ksf1al2')
env.new('sf2al2', 'sextupole', length='lfsxt', k2='ksf2al2')
env.new('sd1al2', 'sextupole', length='ldsxt', k2='ksd1al2')
env.new('sd2al2', 'sextupole', length='ldsxt', k2='ksd2al2')
env.new('sf1bl2', 'sextupole', length='lfsxt', k2='ksf1bl2')
env.new('sf2bl2', 'sextupole', length='lfsxt', k2='ksf2bl2')
env.new('sd1bl2', 'sextupole', length='ldsxt', k2='ksd1bl2')
env.new('sd2bl2', 'sextupole', length='ldsxt', k2='ksd2bl2')
env.new('sf1al3', 'sextupole', length='lfsxt', k2='ksf1al3')
env.new('sf2al3', 'sextupole', length='lfsxt', k2='ksf2al3')
env.new('sd1al3', 'sextupole', length='ldsxt', k2='ksd1al3')
env.new('sd2al3', 'sextupole', length='ldsxt', k2='ksd2al3')
env.new('sf1bl3', 'sextupole', length='lfsxt', k2='ksf1bl3')
env.new('sf2bl3', 'sextupole', length='lfsxt', k2='ksf2bl3')
env.new('sd1bl3', 'sextupole', length='ldsxt', k2='ksd1bl3')
env.new('sd2bl3', 'sextupole', length='ldsxt', k2='ksd2bl3')
env.new('sf1ar2', 'sextupole', length='lfsxt', k2='ksf1ar2')
env.new('sf2ar2', 'sextupole', length='lfsxt', k2='ksf2ar2')
env.new('sd1ar2', 'sextupole', length='ldsxt', k2='ksd1ar2')
env.new('sd2ar2', 'sextupole', length='ldsxt', k2='ksd2ar2')
env.new('sf1br2', 'sextupole', length='lfsxt', k2='ksf1br2')
env.new('sf2br2', 'sextupole', length='lfsxt', k2='ksf2br2')
env.new('sd1br2', 'sextupole', length='ldsxt', k2='ksd1br2')
env.new('sd2br2', 'sextupole', length='ldsxt', k2='ksd2br2')
env.new('sf1ar3', 'sextupole', length='lfsxt', k2='ksf1ar3')
env.new('sf2ar3', 'sextupole', length='lfsxt', k2='ksf2ar3')
env.new('sd1ar3', 'sextupole', length='ldsxt', k2='ksd1ar3')
env.new('sd2ar3', 'sextupole', length='ldsxt', k2='ksd2ar3')
env.new('sf1br3', 'sextupole', length='lfsxt', k2='ksf1br3')
env.new('sf2br3', 'sextupole', length='lfsxt', k2='ksf2br3')
env.new('sd1br3', 'sextupole', length='ldsxt', k2='ksd1br3')
env.new('sd2br3', 'sextupole', length='ldsxt', k2='ksd2br3')
env.new('scrabl', 'sextupole', length='(l_sxtf / 4.0)', k2='kcrabl')
env.new('scrabr', 'sextupole', length='(l_sxtf / 4.0)', k2='kcrabr')
env.new('sfx2r', 'sextupole', length='(l_sxtf / 4.0)', k2='ksfx1r')
env.new('sfx1r', 'sextupole', length='(l_sxtf / 4.0)', k2='ksfx1r')
env.new('sdy2r', 'sextupole', length='(l_sxtd / 4.0)', k2='ksdy1r')
env.new('sdy1r', 'sextupole', length='(l_sxtd / 4.0)', k2='ksdy1r')
env.new('sdm1r', 'sextupole', length='(l_sxtm / 2.0)', k2='ksdm1r')
env.new('sfm2r', 'sextupole', length='(l_sxtm / 2.0)', k2='ksfm2r')
env.new('sfx2l', 'sextupole', length='(l_sxtf / 4.0)', k2='ksfx1l')
env.new('sfx1l', 'sextupole', length='(l_sxtf / 4.0)', k2='ksfx1l')
env.new('sdy2l', 'sextupole', length='(l_sxtd / 4.0)', k2='ksdy1l')
env.new('sdy1l', 'sextupole', length='(l_sxtd / 4.0)', k2='ksdy1l')
env.new('sdm1l', 'sextupole', length='(l_sxtm / 2.0)', k2='ksdm1l')
env.new('sfm2l', 'sextupole', length='(l_sxtm / 2.0)', k2='ksfm2l')

# multipole elements:
env.new('oct0r', 'multipole', knl=[0.0, 0.0, 0.0, 'koct0r'])
env.new('oct1r', 'multipole', knl=[0.0, 0.0, 0.0, 'koct1r'])
env.new('oct2r', 'multipole', knl=[0.0, 0.0, 0.0, 'koct2r'])
env.new('dec1r', 'multipole', knl=[0.0, 0.0, 0.0, 0.0, 'kdec1r'])
env.new('decfr', 'multipole', knl=[0.0, 0.0, 0.0, 0.0, 'kdecfr'])
env.new('decdr', 'multipole', knl=[0.0, 0.0, 0.0, 0.0, 'kdecdr'])
env.new('oct0l', 'multipole', knl=[0.0, 0.0, 0.0, 'koct0l'])
env.new('oct1l', 'multipole', knl=[0.0, 0.0, 0.0, 'koct1l'])
env.new('oct2l', 'multipole', knl=[0.0, 0.0, 0.0, 'koct2l'])
env.new('dec1l', 'multipole', knl=[0.0, 0.0, 0.0, 0.0, 'kdec1l'])
env.new('decfl', 'multipole', knl=[0.0, 0.0, 0.0, 0.0, 'kdecfl'])
env.new('decdl', 'multipole', knl=[0.0, 0.0, 0.0, 0.0, 'kdecdl'])

# drift elements:
env.new('ds_01', 'drift', length='(((dl_len * bxyff) * (1.0 - ads1)) * 0.5)')
env.new('ds_02', 'drift', length='(((dl_len * bxyff) * (1.0 - ads2)) * 0.5)')
env.new('ds_03', 'drift', length='(((dl_len * bxyff) * (1.0 - ads3)) * 0.5)')
env.new('ds_04', 'drift', length='(((dl_len * bxyff) * (((ads1 + ads2) + ads3) - 1.0)) * 0.5)')
env.new('dr_01', 'drift', length=0.15)
env.new('dl_00', 'drift', length=47.0)
env.new('dl_04', 'drift', length=59.369)
env.new('dl_01', 'drift', length=75.0)
env.new('dl_01m', 'drift', length=37.5)
env.new('dl_05', 'drift', length='(66.9 - dd56)')
env.new('dl_06', 'drift', length='(0.2 + dd56)')
env.new('dl_02a', 'drift', length='(7.0 + (clength_adj / 24.0))')
env.new('dl_02b', 'drift', length='(7.0 + (clength_adj / 24.0))')
env.new('dl_02c', 'drift', length='(7.0 + (clength_adj / 24.0))')
env.new('d7l', 'drift', length='((lbfl * 0.72) + 0.3)')
env.new('d4l', 'drift', length='(lbfl * 0.95)')
env.new('d3l', 'drift', length='(lbfl * 0.72)')
env.new('d7r', 'drift', length='((lbfr * 0.84) + 0.3)')
env.new('lx0', 'drift', length=0.15)
env.new('d8l', 'drift', length=7.0)
env.new('d8r', 'drift', length=60.5065)
env.new('d2r', 'drift', length=17.1)
env.new('d2', 'drift', length=17.1)
env.new('d1', 'drift', length=0.15)
env.new('d0', 'drift', length=2.2)

# rfcavity elements:
env.new('rfc', 'rfcavity', length=1e-12, harmon=121200.0, lag='(rf_lag) * 360', voltage='(rf_voltage) * 1e6')

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

env.new_line(name='mark_e_ccsyl', components=[env.new('ccs_y_edge_l', 'Marker')])
env.new_line(name='mark_e_ccsyr', components=[env.new('ccs_y_edge_r', 'Marker')])
env.new_line(name='mark_e_ffl', components=[env.new('ff_edge_l', 'Marker')])
env.new_line(name='mark_e_ffr', components=[env.new('ff_edge_r', 'Marker')])
env.new_line(name='mark_mid_cell_l', components=[env.new('mid_cell_edge_l', 'Marker')])
env.new_line(name='mark_mid_cell_r', components=[env.new('mid_cell_edge_r', 'Marker')])
env.new_line(name='mark_ip_mid', components=[env.new('ip_mid', 'Marker')])
env.new_line(name='mark_ser_ins_l', components=[env.new('serv_inser_edge_l', 'Marker')])
env.new_line(name='mark_ser_ins_r', components=[env.new('serv_inser_edge_r', 'Marker')])
env.new_line(name='mark_ser_ins_mid', components=[env.new('serv_inser_mid', 'Marker')])

env['arc_octant'] = (12 * env['cell_u']
                   + env['mark_mid_cell_l']
                   + env['cell_u']
                   + env['mark_mid_cell_r']
                   + 12 * env['cell_u'])

env['ffl'] = env['ccs_xl'] + env['mark_e_ccsyl'] + env['ccs_yl']
env['ffr'] = env['ccs_xr'] + env['mark_e_ccsyr'] + env['ccs_yr']
env['experimental_insertion_l'] =  (env['cell_l3'] + env['cell_uffl'] + env['mark_e_ffl'] + env['ffl'])
env['experimental_insertion_r'] = -(env['cell_r3'] + env['cell_uffr'] + env['mark_e_ffr'] + env['ffr'])

env['service_insertion_l'] = -(env['cell_ul'] + env['cell_us'] + env['straight_l'])
env['service_insertion_r'] =  (env['cell_ur'] + env['cell_su'] + env['straight_r'])

env['fcc_quarter'] = (
                      env['mark_ip_mid']
                    + env['experimental_insertion_r']
                    + env['arc_octant']
                    + env['mark_ser_ins_r']
                    + env['service_insertion_r']
                    + env['mark_ser_ins_mid']
                    + env['service_insertion_l']
                    + env['mark_ser_ins_l']
                    + env['arc_octant']
                    + env['experimental_insertion_l'])

env['fccee_p_ring'] = 4 * env['fcc_quarter']


env.vars.default_to_zero=False