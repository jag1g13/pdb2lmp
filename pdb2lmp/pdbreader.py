
from collections import namedtuple


class PDBReader:
    def __init__(self, filename):
        with open(filename) as pdb:
            self.atoms = []
            Atom = namedtuple("Atom", ["name", "resname", "resid", "x", "y", "z"])
            self.molecules = []
            Molecule = namedtuple("Molecule", ["name", "atoms"])
            last_resid = -1

            for line in pdb:
                if line.startswith("ATOM  "):
                    self.atoms.append(Atom(line[12:16].strip(),
                                           line[17:20].strip(),
                                           int(line[22:26]),
                                           float(line[30:38]),
                                           float(line[38:46]),
                                           float(line[47:55])))
                    if self.atoms[-1].resid != last_resid:
                        self.molecules.append(Molecule(self.atoms[-1].resname, []))
                        last_resid = self.atoms[-1].resid
                    self.molecules[-1].atoms.append(int(line[6:11])-1)

            self.natoms = len(self.atoms)
            self.nmol = len(self.molecules)
