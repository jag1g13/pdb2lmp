import os

from lib.fileparser import FileParser


class BondDatabase:
    def __init__(self):
        fp = FileParser(os.path.join("data", "bonds.dat"))
        self.lengths = {}
        self.angles = {}

        # Read bond lengths
        while True:
            toks = fp.getlinefromsection("length")
            if toks is None:
                break
            self.lengths[toks[0]] = " ".join(toks[1:])

        # Read angles
        while True:
            toks = fp.getlinefromsection("angle")
            if toks is None:
                break
            self.angles[toks[0]] = " ".join(toks[1:])
