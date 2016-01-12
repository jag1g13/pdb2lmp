import os

from collections import OrderedDict, namedtuple

from ..pdb2lmp.fileparser import FileParser


class MolDatabase:
    data_dir = "data"

    def __init__(self, filename):
        """
        Create a new MolDatabase object

        Args:
            filename: Name of molecule database file to open; GROMACS rtp file.
        """
        fp = FileParser(os.path.join(MolDatabase.data_dir, filename))
        self.molecules = {}
        Atom = namedtuple("Atom", ["name", "type", "charge"])
        Molecule = namedtuple("Molecule", ["name", "atoms", "bonds", "angles", "dihedrals", "impropers"])

        while True:
            mol = fp.nextsection()
            if mol is None:
                break

            self.molecules[mol] = Molecule(mol, OrderedDict(), set(), set(), set(), set())
            natms, nbnds, nangs, ndihs, nimps = fp.getline()

            for i in range(int(natms)):
                toks = fp.getline()
                self.molecules[mol].atoms[toks[0]] = Atom(toks[0], toks[1], float(toks[2]))
