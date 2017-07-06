#spin-log⠶src⠶parse⠶symsem.py

from collections import OrderedDict as OD
# from symdef import symdef as sd

def scansym(line):
    """Parse the line in symlist.mmt corresponding to a 
    symbol pattern 'definition' into a set of properties
    for entry into the index returned as 'symcyl'."""
    if not (line.count('[') == line.count(']') == 2):
        raise ValueError("Symbol {} does not contain 2 pairs of []"
                .format(line))
    prec = (line.find(',') == 1)
    sympre = line[line.find('[')+1:line.find(']')]
    symsuff = line[line.find(']')+2:len(line)-1]
    return prec, sympre, symsuff

class symspec:
    """Class with parsed information from the line in
    symlist.mmt as properties: whether the line has a
    preceding comma (meaning must follow previous line's
    defined symbol pattern), and pre- and suffix patterns"""
    def __init__(self, line):
        self.prec, self.sympre, self.symsuff = scansym(line)
    def __repr__(self):
        return "<symspec::prec:'{}', '{}'::'{}'>"\
            .format(self.prec, self.sympre, self.symsuff)
    def get(self, key, default=None):
        return self.__dict__.get(key, default)

def scansyms(symset):
    """Parse the list of lines from the symlist.mmt ("symset")
    into a list with the previously string-encoded information
    annotated explicitly as properties per line"""
    cyl = []
    for symline in symset:
        cyl.append(symspec(symline))
    return cyl

def scansymsets(symsets):
    """Iterate through the sets of symbol listings, generating
    symspec object lists through calls to scansyms with
    explicitly stored symbol values for robust matching."""
    cyl = []
    for symset in symsets:
        cyl.append(scansyms(symset))
    return cyl

def collatesym(cyl):
    """Collect the entire set of symbols in the cyl data
    structure (potentially one-to-many), for cross-reference
    when matching newly observed lines [i.e. parsing]"""
    symcontexts = OD()
    for i in range(0,len(cyl)):
        c = cyl[i]
        # c = the output of a call to scansyms(symset),
        # i.e. set of <symspec> (containing pre/suffixes)
        for j in range(0,len(c)):
            spec = c[j]
            for sym in (spec.sympre, spec.symsuff):
                if sym not in symcontexts.keys():
                    symcontexts[sym] = []
                symcontexts[sym].append((i,j))
    return symcontexts

class symcyl:
    """Store of indexed symbols for the mmt format,
    implemented using the symspec class per line (entry)
    from the symlist.mmt specification"""
    def __init__(self, symsets):
        self.cyl = scansymsets(symsets)
        self.symcontexts = collatesym(self.cyl)
    def getcontexts(self, sym):
        contexts = self.symcontexts[sym]
        return contexts
        # import symcyl as sc
        # p = sc.scansymlist()
        # p.getcontexts('..')
        # ==> [(3, 0), (4, 0)]
