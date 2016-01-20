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

        self.section(fp, "length", self.lengths)
        self.section(fp, "angle", self.angles)
        self.section(fp, "dihedral", self.dihedrals)
        self.section(fp, "improper", self.impropers)

    @staticmethod
    def section(fp, name, adddict):
        Param = namedtuple("Param", ["style", "params"])
        while True:
            toks = fp.getlinefromsection(name)
            if toks is None:
                break
            adddict[toks[0]] = Param(toks[1], " ".join(toks[2:]))

