import os
from collections import namedtuple

from lib.fileparser import FileParser


class BondDatabase:
    def __init__(self):
        fp = FileParser(os.path.join("data", "bonds.dat"))
        self.lengths = {}
        self.angles = {}
        self.dihedrals = {}
        self.impropers = {}

        Param = namedtuple("Param", ["style", "params"])

        # Read bond lengths
        while True:
            toks = fp.getlinefromsection("length")
            if toks is None:
                break
            self.lengths[toks[0]] = Param(toks[1], " ".join(toks[2:]))

        # Read angles
        while True:
            toks = fp.getlinefromsection("angle")
            if toks is None:
                break
            self.angles[toks[0]] = Param(toks[1], " ".join(toks[2:]))

        while True:
            toks = fp.getlinefromsection("dihedral")
            if toks is None:
                break
            self.dihedrals[toks[0]] = Param(toks[1], " ".join(toks[2:]))

        while True:
            toks = fp.getlinefromsection("improper")
            if toks is None:
                break
            self.impropers[toks[0]] = Param(toks[1], " ".join(toks[2:]))
