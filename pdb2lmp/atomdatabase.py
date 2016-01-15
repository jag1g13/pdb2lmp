import os
from math import sqrt

from collections import defaultdict

from pdb2lmp.fileparser import FileParser
from pdb2lmp.atom import Atom


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

        # Read atom types
        while True:
            toks = fp.getlinefromsection("atomtypes")
            if toks is None:
                break
            self.atoms[toks[0]] = Atom.fromatomdb(toks[0], float(toks[1]), float(toks[2]),
                                                  float(toks[3]), float(toks[4]))

        # Read h-values and produce table
        while True:
            toks = fp.getlinefromsection("nonbond_params")
            if toks is None:
                break
            self.lj_table_eps[toks[0]][toks[1]] = float(toks[2])

    def lj(self, at1, at2):
        # From Lorentz-Berthelot combination - doesn't have h-scaling
        sig = (self.atoms[at1].sig + self.atoms[at2].sig) / 2.

        # Look for various combinations of 2 atoms and X - generic atom
        h = None
        # Try to find as requested
        if at1 in self.lj_table_eps:
            if at2 in self.lj_table_eps[at1]:
                h = self.lj_table_eps[at1][at2]

        # Swapped
        if h is None and at2 in self.lj_table_eps:
            if at1 in self.lj_table_eps[at2]:
                h = self.lj_table_eps[at2][at1]

        # Order requested but generic X in 2nd place
        if h is None and at1 in self.lj_table_eps:
            if "X" in self.lj_table_eps[at1]:
                h = self.lj_table_eps[at1]["X"]

        # Swapped with generic X in 2nd place
        if h is None and at2 in self.lj_table_eps:
            if "X" in self.lj_table_eps[at2]:
                h = self.lj_table_eps[at2]["X"]

        if h is None and "X" in self.lj_table_eps:
            # Order requested but X in first place
            if at2 in self.lj_table_eps["X"]:
                h = self.lj_table_eps["X"][at2]
            # Swapped with X in 1st place
            if at1 in self.lj_table_eps["X"]:
                h = self.lj_table_eps["X"][at1]
            # X in both places
            elif "X" in self.lj_table_eps["X"]:
                h = self.lj_table_eps["X"]["X"]

        # Not in table - assume 1
        if h is None:
            h = 1

        eps = h * sqrt(self.atoms[at1].eps * self.atoms[at2].eps)

        return sig, eps
