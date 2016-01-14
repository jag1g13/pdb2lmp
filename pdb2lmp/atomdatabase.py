import os
from math import sqrt

from collections import defaultdict

from ..pdb2lmp.fileparser import FileParser
from ..pdb2lmp.atom import Atom


class AtomDatabase:
    def __init__(self):
        """
        Create a new AtomDatabase object

        Args:
            filename: Name of atom database file to open; GROMACS rtp file.
        """
        fp = FileParser(os.path.join("data", "atoms.dat"))
        self.atoms = {}
        self.lj_table_eps = defaultdict(dict)

        while True:
            toks = fp.getlinefromsection("atomtypes")
            if toks is None:
                break
            self.atoms[toks[0]] = Atom.fromdb(toks[0], float(toks[1]), float(toks[2]),
                                              float(toks[3]), float(toks[4]))

        while True:
            toks = fp.getlinefromsection("nonbond_params")
            if toks is None:
                break
            self.lj_table_eps[toks[0]][toks[1]] = float(toks[3])


    def lj(self, at1, at2):
        # From Lorentz-Berthelot combination - doesn't have h-scaling
        sig = (self.atoms[at1].sig + self.atoms[at2].sig) / 2.

        eps = None
        # Look for various combinations of 2 atoms and X - generic atom
        if at1 in self.lj_table_eps:
            if at2 in self.lj_table_eps[at1]:
                eps = self.lj_table_eps[at1][at2]
            elif "X" in self.lj_table_eps[at1]:
                eps = self.lj_table_eps[at1]["X"]

        elif "X" in self.lj_table_eps:
            if at2 in self.lj_table_eps["X"]:
                eps = self.lj_table_eps["X"][at2]
            elif "X" in self.lj_table_eps["X"]:
                eps = self.lj_table_eps["X"]["X"]

        elif at2 in self.lj_table_eps:
            if at1 in self.lj_table_eps[at2]:
                eps = self.lj_table_eps[at2][at1]
            elif "X" in self.lj_table_eps[at2]:
                eps = self.lj_table_eps[at2]["X"]

        # If not found assume Lorentz-Berthelot combination
        if eps is None:
            eps = sqrt(self.atoms[at1].eps * self.atoms[at2].eps)

        return (sig, eps)
