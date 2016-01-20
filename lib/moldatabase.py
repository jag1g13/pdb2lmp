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
        Length = namedtuple("Length", ["type", "atom1", "atom2"])
        Angle = namedtuple("Length", ["type", "atom1", "atom2", "atom3"])
        Dihedral = namedtuple("Length", ["type", "atom1", "atom2", "atom3", "atom4"])
        Improper = namedtuple("Length", ["type", "atom1", "atom2", "atom3", "atom4"])

        while True:
            mol = fp.nextsection()
            if mol is None:
                break

            self.molecules[mol] = Molecule(OrderedDict(), [], [], [], [])
            natms, nbnds, nangs, ndihs, nimps = fp.getline(5)

            if natms is not None:
                for i in range(int(natms)):
                    toks = fp.getline()
                    self.molecules[mol].atoms[toks[0]] = Atom.frommoldb(toks[0], toks[1], float(toks[2]))

            if nbnds is not None:
                for i in range(int(nbnds)):
                    toks = fp.getline()
                    self.molecules[mol].lengths.append(Length(toks[0], toks[1], toks[2]))

            if nangs is not None:
                for i in range(int(nangs)):
                    toks = fp.getline()
                    self.molecules[mol].angles.append(
                            Angle(toks[0], toks[1], toks[2], toks[3]))

            if ndihs is not None:
                for i in range(int(ndihs)):
                    toks = fp.getline()
                    self.molecules[mol].dihedrals.append(
                            Dihedral(toks[0], toks[1], toks[2], toks[3], toks[4]))

            if nimps is not None:
                for i in range(int(nimps)):
                    toks = fp.getline()
                    self.molecules[mol].impropers.append(
                            Improper(toks[0], toks[1], toks[2], toks[3], toks[4]))
