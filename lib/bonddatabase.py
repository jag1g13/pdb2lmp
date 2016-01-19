import os
from collections import namedtuple

from lib.fileparser import FileParser


class BondDatabase:
    def __init__(self):
        fp = FileParser(os.path.join("data", "bonds.dat"))
        self.lengths = {}
        self.angles = {}

        Length = namedtuple("Length", ["style", "k", "r"])
        Angle = namedtuple("Length", ["style", "k", "r"])

        # Read bond lengths
        while True:
            toks = fp.getlinefromsection("length")
            if toks is None:
                break
            self.lengths[toks[0]] = Length(toks[1], float(toks[2]), float(toks[3]))

        # Read angles
        while True:
            toks = fp.getlinefromsection("angle")
            if toks is None:
                break
            self.angles[toks[0]] = Angle(toks[1], float(toks[2]), float(toks[3]))
