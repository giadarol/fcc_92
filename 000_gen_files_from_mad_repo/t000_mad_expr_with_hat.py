from cpymad.madx import Madx
from xtrack.mad_parser.loader import MadxLoader

loader = MadxLoader()
loader.load_string('''a=4;
                   b := a^2;
                   c := (a)^2.;
                   d := a ^ 2;
                   seq: sequence, l = 1;
                   m: marker;
                   endsequence;
                   ''')

env = loader.env

env.get_expr('b')
# is vars['a^2'] <-- this is not correct!!!!

env.get_expr('c')
# vars['a'] ** 2.0) <-- this is correct

env.get_expr('d')
# vars['a'] ** 2.0) <-- this is correct