def scanmmd(filename):
    """Pass in a filename (or full path) to a .mmd file
    and return a list of its lines"""
    with open(filename) as f:
        mmdlines = f.readlines()
    return mmdlines

def buildAST(mmdlines):
    """Pass in a list of lines from an .mmd file
    and return an AST of the .mmd format"""
    linecount = len(mmdlines)
    # NB: prototype will just return the no. of lines
    # until the dictionary of symbols is built in mmdcyl.py
    # loaded from storage in symlist.mmt by parsemmt.py
    return linecount
