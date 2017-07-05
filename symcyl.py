

from symsem import mmddict

# hard coded symbol list
symlist = 'symlist.mmt'

def scanpranges(mmtlines):
    blanks = [i for i, x in enumerate(mmtlines) if x == '']
    # build the 'paragraphs' over the ranges segmented by blanks
    lower_bound = 0
    # store the range start/stop indices [as pairs] in an array
    pranges = []
    for b in blanks:
        while lower_bound in blanks:
            lower_bound += 1
        if lower_bound > b:
            continue
        upper_bound = b - 1
        prange = (lower_bound, upper_bound)
        pranges.append(prange)
        lower_bound = b + 1
        # for the final blank, go to the end
        if b == blanks[len(blanks)-1]:
            # if the last blank is on the last line then finish
            # otherwise create a final range up to the final line
            if lower_bound != len(mmtlines):
                upper_bound = len(mmtlines) - 1
                prange = (lower_bound, upper_bound)
                pranges.append(prange)
    return pranges

def scansymranges(mmtlines, pranges):
    symsets = []
    for prange in pranges:
        symsets.append(mmtlines[prange[0]:prange[1]+1])
    return symsets

def parsemmt(mmtlines):
    pranges = scanpranges(mmtlines)
    symsets = scansymranges(mmtlines, pranges)
    symdict = {'pranges': pranges, 'symsets': symsets}
    return symdict

def scansymlist():
    """Load symlist and return as a dictionary"""
    with open(symlist) as f:
        mmtlines = [l.rstrip('\n') for l in f]
    symdict = parsemmt(mmtlines)
    return symdict

def buildAST(mmtlines):
    """Pass in a list of lines from an .mmt file
    and return an AST of the .mmd format"""
    linecount = len(mmtlines)
    # NB: prototype will just return the no. of lines
    # until the dictionary of symbols is built in mmdcyl.py
    # loaded from storage in symlist.mmt by parsemmt.py
    return linecount
