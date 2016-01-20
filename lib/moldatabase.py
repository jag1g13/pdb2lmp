import os

from collections import OrderedDict, namedtuple

from lib.fileparser import FileParser
from lib.atom import Atom


class MolDatabase:
    def __init__(self):
        """
        Create a new MolDatabase object

        Args:
            filename: Name of molecule database file to open; GROMACS rtp file.
        """
        fp = FileParser(os.path.join("data", "mol.dat"))
        self.molecules = {}
        Molecule = namedtuple("Molecule", ["atoms", "lengths", "angles", "dihedrals", "impropers"])

        while True:
            mol = fp.nextsection()
            if mol is None:
                break

            self.molecules[mol] = Molecule(OrderedDict(), [], [], [], [])
            natms, nbnds, nangs, ndihs, nimps = fp.getline(5)

            if natms is not None:
                for i in range(int(natms)):
                    toks = fp.getline(3)
                    if toks[2] is None:
                        toks[2] = "0"
                    self.molecules[mol].atoms[toks[0]] = Atom.frommoldb(toks[0], toks[1], float(toks[2]))

            self.get_bonds(fp, nbnds, self.molecules[mol].lengths)
            self.get_bonds(fp, nangs, self.molecules[mol].angles)
            self.get_bonds(fp, ndihs, self.molecules[mol].dihedrals)
            self.get_bonds(fp, nimps, self.molecules[mol].impropers)

    @staticmethod
    def get_bonds(fp, n, store):
        Bond = namedtuple("Bond", ["type", "atom1", "atom2", "atom3", "atom4"])
        if n is not None:
            for i in range(int(n)):
                toks = fp.getline(5)
                store.append(Bond(*toks))
