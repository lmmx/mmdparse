#spin-log⠶src⠶parse⠶symdef.py

# This file provides the 'definition' to the symbol
# syntax laid out in symsem.py and gathered into
# a data structure in symcyl.py

# N.B. 'symspec' is 'spec' as in 'specification' not
# 'special', which here denotes four particular values

class matcher:
    def __init__(self, symbol, posfunc):
        self.symbol = symbol
        self.posfunc = posfunc

def m_wc(symbol, posfunc):
    """Special match function: hyphen with wildcard
    (i.e. hyphen then anything - note that in reality
    this only works at the start of the line, which 
    is all it needs to do, but not quite 'wildcard').

    After thinking about it, there isn't quite the
    specific enough implementation to warrant this
    (i.e. without the wildcard would suffice) but
    in this notation spec I wanted to express that
    other patterns mean 'this and only this' whereas
    this wildcard has multiple meanings). TBC maybe."""
    m = matcher(symbol='-', posfunc=posfunc)
    return m

def m_x(symbol, posfunc):
    """Special match function: omit pattern entirely
    (i.e. use the other pattern to match entire line).
    Stated more clearly, don't try and match start and
    end separately, instead match entire line."""
    # weird but comprehensible: use str.__ne__ to mean
    # "don't match this [pre/suffix], only the other
    m = matcher(symbol=None, posfunc=str.__ne__)
    return m

def m_sp(symbol, posfunc):
    """Special match function: non-matching (i.e. only
    use the other pattern, to match the other end)"""
    m = matcher(symbol=None, posfunc=None)
    return m

def m_em(symbol, posfunc):
    """Special match function: empty string match (i.e.
    to be used in combination with the pattern omission
    match - 'x' - to specify a match to a blank line)"""
    m = matcher(symbol=symbol, posfunc=str.__eq__)
    return m

specials = {'-*': m_wc,'x': m_x,' ': m_sp, '': m_em}

def specialmatch(symbol, target, posfunc=None):
    m = specials[symbol](symbol, target, posfunc)
    return m

def symmatch(sym, target, posfunc=None):
    # TODO: think carefully about pre/suff matching
    if sym.special:
        specialmatch(sym.symbol, target)
    # ...

class symdef:
    """Defined behaviour for symbol parsing
    according to whether any are in the 'special'
    set, or else to use standard string matching."""
    def __init__(self, symspec):
        self.pre = syminterp(symspec.sympre)
        self.suff = syminterp(symspec.symsuff)

    def match(self, target):
        mp = symmatch(self.pre, target)
        ms = symmatch(self.suff, target)
        m = symmatch()
        return m

class syminterp:
    """Interpret the match pattern symbols.
    
    Symbols with non-standard interpretations are:
    '-*' (asterisk: '-' with wildcard), ' ' (space: any),
    'x' (cross: omit pattern), '' (empty: no content)."""
    def __init__(self, symbol):
        self.symbol = symbol
        self.special = (symbol in specials.keys())
