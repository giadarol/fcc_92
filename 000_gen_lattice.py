import xtrack as xt
from xtrack.mad_parser.parse import MadxParser

parser = MadxParser()

fname = '../fcc-ee-lattice/lattices/z/fccee_z.seq'

with open(fname, 'r') as fid:
    lines = fid.readlines()

# Remove lines containing the "LINE" command (not yet implemented)
lines = [ll for ll in lines if 'LINE=' not in ll.replace(' ', '')]

dct = parser.parse_string('\n'.join(lines))
