import os
from collections import namedtuple

from pdb2lmp.fileparser import FileParser


class BondDatabase:
    def __init__(self):
        fp = FileParser(os.path.join("data", "bonds.dat"))
        self.lengths = {}
        Length = namedtuple("Length", ["name", "type", "k", "r"])

        # Read bond lengths
        while True:
            toks = fp.getlinefromsection("length")
            if toks is None:
                break
            self.lengths[toks[0]] = Length(toks[0], toks[1], float(toks[2]), float(toks[3]))
