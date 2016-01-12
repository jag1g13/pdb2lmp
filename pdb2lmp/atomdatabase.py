import os

from collections import namedtuple

from ..pdb2lmp.fileparser import FileParser


class AtomDatabase:
    data_dir = "data"

    def __init__(self, filename):
        """
        Create a new AtomDatabase object

        Args:
            filename: Name of atom database file to open; GROMACS rtp file.
        """
        fp = FileParser(os.path.join(AtomDatabase.data_dir, filename))
        self.atoms = {}
        Atom = namedtuple("Atom", ["type", "mass", "charge", "sig", "eps", "lj"])

        while True:
            toks = fp.getlinefromsection("atomtypes")
            if toks is None:
                break
            self.atoms[toks[0]] = Atom(toks[0], float(toks[1]), float(toks[2]),
                                       float(toks[3]), float(toks[4]), {})
