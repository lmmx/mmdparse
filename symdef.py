#spin-log⠶src⠶parse⠶symdef.py

# This file provides the 'definition' to the symbol
# syntax laid out in symsem.py and gathered into
# a data structure in symcyl.py

# N.B. 'symspec' is 'spec' as in 'specification' not
# 'special', which here denotes four particular values

specials = ['-*','x',' ','']

class symdef:
    """Defined behaviour for symbol parsing
    according to whether any are in the 'special'
    class, or else to use standard string matching."""
    def __init__(self, symspec):
        self.pre = symspec.sympre
        self.suff = symspec.symsuff
        self.p_special = special(self.pre)
        self.s_special = special(self.suff)
    def match(self, other):
        if self.p_special is None:
            # use self.pre
        else:
            # use self.p_special
        if self.s_special is None:
            # use self.suff
        else:
            # use self.s_special

class special:
    """Symbols with non-standard interpretations:
    '-*' (asterisk: wildcard), ' ' (space: ),
    'x' (cross: omit pattern), '' (empty: no content)."""
    def __init__(self, symbol):
        self.symdict = 
