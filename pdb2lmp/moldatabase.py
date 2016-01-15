import os

from collections import OrderedDict, namedtuple

from pdb2lmp.fileparser import FileParser
from pdb2lmp.atom import Atom


class MolDatabase:
    def __init__(self):
        """
        Create a new MolDatabase object

        Args:
            filename: Name of molecule database file to open; GROMACS rtp file.
        """
        fp = FileParser(os.path.join("data", "mol.rtp"))
        self.molecules = {}
        Molecule = namedtuple("Molecule", ["name", "atoms", "bonds", "angles", "dihedrals", "impropers"])

        while True:
            mol = fp.nextsection()
            if mol is None:
                break

            self.molecules[mol] = Molecule(mol, OrderedDict(), set(), set(), set(), set())
            natms, nbnds, nangs, ndihs, nimps = fp.getline(5)

            if natms is not None:
                for i in range(int(natms)):
                    toks = fp.getline()
                    self.molecules[mol].atoms[toks[0]] = Atom.frommoldb(toks[0], toks[1], float(toks[2]))
