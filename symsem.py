#spin-log⠶src⠶parse⠶symsem.py

def scansym(line):
    """Parse the line in symlist.mmt corresponding to a 
    symbol pattern 'definition' into a set of properties
    for entry into the dictionary returned as 'symdict'."""
    if not (line.count('[') == line.count(']') == 2):
        print("Symbol {} does not contain 2 pairs of []!"
                .format(line))
        break
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
        self.prec, self.symstart, self.symend = scansym(line)

class symset:
    """Set of classes with information on the symbols
    associated with one another in the symlist.mmt spec.
    Each line implements the symspec class."""
    def __init__(self, symset):
        # split the symset into symbols using symspec
        self.

class symdict:
    """Dictionary of indexed symbols for the mmt format,
    implements a symbol dictionary using the symspec class"""
    def __init__(self, symsets):
        self.dict = scansymsets(symsets)

def scansymsets(symsets):
    """..."""
    for symset in symsets:
        symcyl = scansyms(symset)

def scansyms(symset):
    """Parse the list of lines from the symlist.mmt ("symset")
    into a list with the previously string-encoded information
    annotated explicitly as properties per line"""
    symsem = []
    for symline in symset:
        symsem.append(symspec(sym))
