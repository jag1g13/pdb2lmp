from collections import namedtuple

from lib.atom import Atom


class PDBReader:
    def __init__(self, filename):
        self.atoms = []
        self.molecules = []
        self.cell = []

        with open(filename) as pdb:
            Molecule = namedtuple("Molecule", ["name", "atoms"])
            last_resid = -1

            for line in pdb:
                if line.startswith("ATOM  "):
                    self.atoms.append(Atom.frompdb(line[12:16].strip(),
                                                   line[17:20].strip(),
                                                   int(line[22:26]),
                                                   float(line[30:38]),
                                                   float(line[38:46]),
                                                   float(line[47:55])))
                    if self.atoms[-1].resid != last_resid:
                        self.molecules.append(Molecule(self.atoms[-1].resname, []))
                        last_resid = self.atoms[-1].resid
                    self.molecules[-1].atoms.append(int(line[6:11])-1)

                if line.startswith("CRYST1"):
                    self.cell = [float(line[6:15]), float(line[15:24]), float(line[24:33]),
                                 float(line[33:40]), float(line[40:47]), float(line[47:54])]

        self.natoms = len(self.atoms)
        self.nmol = len(self.molecules)
