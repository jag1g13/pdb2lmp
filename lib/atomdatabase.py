import os
from math import sqrt

from collections import defaultdict

from lib.json import Parser
from lib.atom import Atom


class AtomDatabase:
    def __init__(self, filename=None):
        """
        Create a new AtomDatabase object

        Args:
            filename: Name of atom database file to open.
        """
        if filename is None:
            filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                    os.path.join("data", "atoms.json"))

        db = Parser(filename)
        self.atoms = {}
        self._lj_table_eps = defaultdict(dict)

        # Read atom types
        for name, data in db.atoms.items():
            if "rotmass" not in data:
                data.rotmass = data.mass
            self.atoms[name] = Atom(type=name, **data)

        for name1, atom1 in self.atoms.items():
            for name2, atom2 in self.atoms.items():

                try:
                    h = db.h_values[name1][name2]
                except KeyError:
                    try:
                        h = db.h_values[name2][name1]
                    except KeyError:
                        h = 1.

                self._lj_table_eps[name1][name2] = h * sqrt(atom1.epsilon * atom2.epsilon)

    def lj(self, at1, at2):
        """
        Return Lennard-Jones sigma and epsilon values for a bead pair using Lorentz-Berthelot combination.
        Args:
            at1: First atom/bead
            at2: Second atom/bead

        Returns:
            (sigma, epsilon)
        """
        sig = (self.atoms[at1].sigma + self.atoms[at2].sigma) / 2.

        return sig, self._lj_table_eps[at1][at2]
