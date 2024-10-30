import xtrack as xt

env = xt.Environment()

env.call('fccee_z_parameters.py')
env.call('fccee_z_elements.py')
env.call('fccee_z_lattice.py')
env.call('fccee_z_strengths.py')

line = env['fccee_p_ring']
line0 = line.copy()

section = line.select('mid_cell_edge_r::0','mid_cell_edge_l::1')
cell0 = line.select('mid_cell_edge_l::0','mid_cell_edge_r::0')
cell1 = line.select('mid_cell_edge_l::1','mid_cell_edge_r::1')

tw_cell_0 = cell0.twiss4d()
twinit_cell_0_r = tw_cell_0.get_twiss_init('mid_cell_edge_r')
tw_cell_1 = cell0.twiss4d()
twinit_cell_1_l = tw_cell_1.get_twiss_init('mid_cell_edge_l')

tw0 = section.twiss(init=twinit_cell_0_r,
                    compute_chromatic_properties=True,
                    strengths=True)

tt0 = section.get_table(attr=True)
tt0_quad = tt0.rows[tt0.element_type == 'Quadrupole']
tt0_sext = tt0.rows[tt0.element_type == 'Sextupole']

# Inspect sextupoles in special arc cells
sl_match = [
    'sd2aur', 'sf1aur', 'sd1aur', 'sf2aur',
    'sf2asr', 'sd1asr', 'sf1asr', 'sd2asr',
    'sf3asr',
    'sf3asl', 'sd2asl', 'sf1asl', 'sd1asl',
    'sf2asl', 'sf2aul', 'sd1aul', 'sf1aul',
    'sd2aul'
]

for ss in sl_match:
    ee = env[ss].get_expr('k2')
    print(ss, ee, ee._expr)

# sd2aur vars['ksd2ur'] ((vars['ksdfam2'] + ((0.0 * vars['dogleg_on']) * vars['sxt_on'])) + (0.058 * vars['sxt_on']))
# sf1aur vars['ksf1ur'] ((vars['ksffam1'] + ((0.0 * vars['dogleg_on']) * vars['sxt_on'])) - (0.011 * vars['sxt_on']))
# sd1aur vars['ksd1ur'] ((vars['ksdfam1'] - ((0.008 * vars['dogleg_on']) * vars['sxt_on'])) + (0.058 * vars['sxt_on']))
# sf2aur vars['ksf2ur'] ((vars['ksffam2'] - ((0.0 * vars['dogleg_on']) * vars['sxt_on'])) - (0.011 * vars['sxt_on']))
# sf2asr vars['ksf2sr'] ((vars['ksffam2'] - ((0.044 * vars['dogleg_on']) * vars['sxt_on'])) + (0.124 * vars['sxt_on']))
# sd1asr vars['ksd1sr'] ((vars['ksdfam1'] + ((0.008 * vars['dogleg_on']) * vars['sxt_on'])) - (0.058 * vars['sxt_on']))
# sf1asr vars['ksf1sr'] ((vars['ksffam1'] - ((0.044 * vars['dogleg_on']) * vars['sxt_on'])) - (0.092 * vars['sxt_on']))
# sd2asr vars['ksd2sr'] (((vars['ksdfam2'] * 0.0) + ((0.0 * vars['dogleg_on']) * vars['sxt_on'])) + (0.0 * vars['sxt_on']))
# sf3asr vars['ksf3sr'] None
# sf3asl vars['ksf3sl'] None
# sd2asl vars['ksd2sl'] (((vars['ksdfam2'] * 0.0) - ((0.0 * vars['dogleg_on']) * vars['sxt_on'])) + (0.0 * vars['sxt_on']))
# sf1asl vars['ksf1sl'] ((vars['ksffam1'] + ((0.044 * vars['dogleg_on']) * vars['sxt_on'])) - (0.092 * vars['sxt_on']))
# sd1asl vars['ksd1sl'] ((vars['ksdfam1'] - ((0.008 * vars['dogleg_on']) * vars['sxt_on'])) - (0.058 * vars['sxt_on']))
# sf2asl vars['ksf2sl'] ((vars['ksffam2'] + ((0.044 * vars['dogleg_on']) * vars['sxt_on'])) + (0.124 * vars['sxt_on']))
# sf2aul vars['ksf2ul'] ((vars['ksffam2'] + ((0.0 * vars['dogleg_on']) * vars['sxt_on'])) - (0.011 * vars['sxt_on']))
# sd1aul vars['ksd1ul'] ((vars['ksdfam1'] + ((0.008 * vars['dogleg_on']) * vars['sxt_on'])) + (0.058 * vars['sxt_on']))
# sf1aul vars['ksf1ul'] ((vars['ksffam1'] - ((0.0 * vars['dogleg_on']) * vars['sxt_on'])) - (0.011 * vars['sxt_on']))
# sd2aul vars['ksd2ul'] ((vars['ksdfam2'] - ((0.0 * vars['dogleg_on']) * vars['sxt_on'])) + (0.058 * vars['sxt_on']))

env.vars.default_to_zero = True
env['ksd2ur'] = 'ksdfam2 + ksd2ur_delta'
env['ksf1ur'] = 'ksffam1 + ksf1ur_delta'
env['ksd1ur'] = 'ksdfam1 + ksd1ur_delta'
env['ksf2ur'] = 'ksffam2 + ksf2ur_delta'
env['ksf2sr'] = 'ksffam2 + ksf2sr_delta'
env['ksd1sr'] = 'ksdfam1 + ksd1sr_delta'
env['ksf1sr'] = 'ksffam1 + ksf1sr_delta'
env['ksf1sl'] = 'ksffam1 + ksf1sl_delta'
env['ksd1sl'] = 'ksdfam1 + ksd1sl_delta'
env['ksf2sl'] = 'ksffam2 + ksf2sl_delta'
env['ksf2ul'] = 'ksffam2 + ksf2ul_delta'
env['ksd1ul'] = 'ksdfam1 + ksd1ul_delta'
env['ksf1ul'] = 'ksffam1 + ksf1ul_delta'
env['ksd2ul'] = 'ksdfam2 + ksd2ul_delta'
env.vars.default_to_zero = False

left_knobs = [
    'ksd2ur_delta', 'ksf1ur_delta', 'ksd1ur_delta', 'ksf2ur_delta',
    'ksf2sr_delta', 'ksd1sr_delta', 'ksf1sr_delta', 'ksf1sl_delta',
    'ksd1sl_delta', 'ksf2sl_delta', 'ksf2ul_delta', 'ksd1ul_delta',
    'ksf1ul_delta', 'ksd2ul_delta'
]
right_knobs = [
    'ksd2ur_delta', 'ksf1ur_delta', 'ksd1ur_delta', 'ksf2ur_delta',
    'ksf2sr_delta', 'ksd1sr_delta', 'ksf1sr_delta', 'ksf1sl_delta',
    'ksd1sl_delta', 'ksf2sl_delta', 'ksf2ul_delta', 'ksd1ul_delta',
    'ksf1ul_delta', 'ksd2ul_delta'
]

tw = section.twiss(init=twinit_cell_0_r,
                    compute_chromatic_properties=True,
                    strengths=True)

opt_close_w = section.match(
    name='close',
    solve=False,
    init=twinit_cell_0_r,
    compute_chromatic_properties=True,
    vary=xt.VaryList(left_knobs + right_knobs, step=1e-4),
    targets=[xt.TargetSet(
                ax_chrom=twinit_cell_0_r.ax_chrom,
                ay_chrom=twinit_cell_0_r.ay_chrom,
                bx_chrom=twinit_cell_0_r.bx_chrom,
                by_chrom=twinit_cell_0_r.by_chrom,
                ddx=twinit_cell_0_r.ddx,
                ddpx=twinit_cell_0_r.ddpx,
                at=xt.END),
    ]
)
opt = opt_close_w
opt.step(10)