#spin-log⠶src⠶parse⠶symdef.py

# This file provides the 'definition' to the symbol
# syntax laid out in symsem.py and gathered into
# a data structure in symcyl.py

# N.B. 'symspec' is 'spec' as in 'specification' not
# 'special', which here denotes four particular values

class matcher:
    """Store the info required to make a match
    in combination with another matcher [for the
    start and end of a line, or to annul one] in
    a call to the match function."""
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

def specialmatch(symbol, posfunc=None):
    """Some symbols are special, and so they receive
    a matcher class according to the functions stored
    in the 'specials' dict (whose keys are symbols)."""
    m = specials[symbol](symbol, posfunc)
    return m

def simplematch(symbol, posfunc=None):
    """Let symbols be symbols, no funny business. Pass
    args unaltered to the matcher class constructor."""
    m = matcher(symbol=symbol, posfunc=posfunc)
    return m

def symmatch(sym, posfunc=None):
    """Function to create matcher objects for either
    prefix or suffix symbols, ultimately to define
    behaviour for the symdef class match method, to
    take effect over an entire line. Precedence is
    not handled here (management of whether a pattern
    appears following another)."""
    if sym.special:
        m = specialmatch(sym.symbol, posfunc)
    else:
        m = simplematch(sym.symbol, posfunc)
    return m

def linematch(target, mpre, msuff):
    """Interpret both matcher items to return a
    boolean [whether the line matches the pattern]
    
    'target' is a string, while 'mpre' and 'msuff'
    should both be <matcher> objects."""
    # series of checks to do before simple 'posfunc'
    # positional match functions can be used:
    # - if either symbol is [x], we ignore it
    #   - it will have str.__ne__ as its posfunc
    # - if either symbol is [ ], it always matches
    #   - it will have 'None' as its posfunc
    #
    # the other two special cases are not treated
    # differently to simple match, so no problem
    pm = ps = None
    if mpre.posfunc is str.__ne__:
        # rely on msuff to match
        # signal so by leaving pm equal to 'None'
        pass
    else if mpre.posfunc is None:
        # it always 'matches'
        pm = True
    else:
        pm = mpre.posfunc(target, mpre.symbol)
    if msuff.posfunc is str.__ne__:
        # rely on mpre to match
        pass
    else if msuff.posfunc is None:
        # [100 emoji]
        ps = True
    else:
        ps = msuff.posfunc(target, msuff.symbol)
    # if both pre & post were [x] raise an error!
    if (pm is ps is None):
        raise ValueError("Config error: both start\
        and end of line symbols can't be '[x]'. \
        Fix the symbol list ('symlist.mmt').")
    else if ((pm is None) or (ps is None)):
        if pm is None:
            return ps
        else:
            # ps is None
            return pm
    if pm and ps:
        return True
    else:
        return False

class symdef:
    """Defined behaviour for symbol parsing
    according to whether any are in the 'special'
    set, or else to use standard string matching."""
    def __init__(self, symspec):
        self.pre = syminterp(symspec.sympre)
        self.suff = syminterp(symspec.symsuff)

    def match(self, target):
        mp = symmatch(self.pre, str.startswith)
        ms = symmatch(self.suff, str.endswith)
        m = linematch(target, mp, ms)
        return m

class syminterp:
    """Interpret the match pattern symbols.
    
    Symbols with non-standard interpretations are:
    '-*' (asterisk: '-' with wildcard), ' ' (space: any),
    'x' (cross: omit pattern), '' (empty: no content)."""
    def __init__(self, symbol):
        self.symbol = symbol
        self.special = (symbol in specials.keys())
