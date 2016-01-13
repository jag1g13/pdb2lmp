
from collections import namedtuple


class PDBReader:
    def __init__(self, filename):
        with open(filename) as pdb:
            self.atoms = []
            Atom = namedtuple("Atom", ["name", "resname", "resid", "x", "y", "z"])

            for line in pdb:
                if line.startswith("ATOM  "):
                    self.atoms.append(Atom(line[12:16].strip(),
                                           line[17:20].strip(),
                                           int(line[22:26]),
                                           float(line[30:38]),
                                           float(line[38:46]),
                                           float(line[47:55])))
            self.natoms = len(self.atoms)
