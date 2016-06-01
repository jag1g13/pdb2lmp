from collections import namedtuple

from lib.atom import Atom

Molecule = namedtuple("Molecule", ["name", "atoms"])


class CoordReader:
    def __init__(self):
        self.atoms = []
        self.molecules = []
        self.cell = []

    @property
    def natoms(self):
        return len(self.atoms)

    @property
    def nmol(self):
        return len(self.molecules)


class PDBReader(CoordReader):
    def __init__(self, filename):
        super(PDBReader, self).__init__()

        with open(filename) as f:
            last_resid = -1

            for line in f:
                if line.startswith("ATOM  "):
                    self.atoms.append(Atom(name=line[13:17].strip(),
                                           resname=line[17:21].strip(),
                                           resid=int(line[22:26]),
                                           x=float(line[30:38]),
                                           y=float(line[38:46]),
                                           z=float(line[46:54])))
                    if self.atoms[-1].resid != last_resid:
                        self.molecules.append(Molecule(self.atoms[-1].resname, []))
                        last_resid = self.atoms[-1].resid
                    self.molecules[-1].atoms.append(int(line[6:11])-1)

                if line.startswith("CRYST1"):
                    self.cell = [float(line[6:15]), float(line[15:24]), float(line[24:33]),
                                 float(line[33:40]), float(line[40:47]), float(line[47:54])]


class GROReader(CoordReader):
    def __init__(self, filename):
        super(GROReader, self).__init__()

        with open(filename) as f:
            last_resid = -1
            self.comment = f.readline()
            natoms = int(f.readline())

            for i in range(natoms):
                line = f.readline()
                self.atoms.append(Atom(name=line[10:15].strip(),
                                       resname=line[5:10].strip(),
                                       resid=int(line[0:5]),
                                       x=10*float(line[20:28]),
                                       y=10*float(line[28:36]),
                                       z=10*float(line[36:44])))
                if self.atoms[-1].resid != last_resid:
                    self.molecules.append(Molecule(self.atoms[-1].resname, []))
                    last_resid = self.atoms[-1].resid
                self.molecules[-1].atoms.append(int(line[15:20])-1)

            line = f.readline()
            self.cell = [10*float(line[0:10]), 10*float(line[10:20]), 10*float(line[20:30])]
