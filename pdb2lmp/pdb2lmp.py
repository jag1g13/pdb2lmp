from collections import namedtuple

from ..pdb2lmp.pdbreader import PDBReader
from ..pdb2lmp.moldatabase import MolDatabase
from ..pdb2lmp.atomdatabase import AtomDatabase


class NonMatchingAtomException(Exception):
    pass


class Counter:
    __slots__ = ["total", "types"]

    def __init__(self, total=0, types=0):
        self.total = 0
        self.types = 0


class PDB2LMP:
    def __init__(self, pdbname):
        self.pdb = PDBReader(pdbname)
        self.moldb = MolDatabase()
        self.atomdb = AtomDatabase()

        self.moltypes = []
        self.atomtypes = []

        self.atoms = Counter(0, 0)

    def collect_types(self):
        atnum = 0
        for mol in self.pdb.molecules:
            if mol.name not in self.moltypes:
                self.moltypes.append(mol.name)
            for atom in self.moldb.molecules[mol.name].atoms:
                if atom.type not in self.atomtypes:
                    self.atomtypes.append(atom.type)
                    self.atoms.types += 1
                if self.pdb.atoms[atnum].name != atom.name:
                    raise NonMatchingAtomException("Atom in PDB ({0}) does not match atom in force field ({1}).".
                                                   format(self.pdb.atoms[atnum].name, atom.name))
                self.atoms.total += 1
                atnum += 1

    def write_data(self, filename):
        with open(filename, "w") as data:
            data.write("LAMMPS 'data.' input file created by PDB2LMP\n")
            data.write("\n")
            data.write("{0:8d} atoms\n".format(self.atoms.total))
            data.write("{0:8d} bonds\n".format(0))
            data.write("{0:8d} angles\n".format(0))
            data.write("{0:8d} dihedrals\n".format(0))
            data.write("{0:8d} impropers\n".format(0))
            data.write("\n")
            data.write("{0:8d} atom types\n".format(self.atoms.types))
            data.write("{0:8d} bond types\n".format(0))
            data.write("{0:8d} angle types\n".format(0))
            data.write("{0:8d} dihedral types\n".format(0))
            data.write("{0:8d} improper types\n".format(0))
            data.write("\n")
            data.write("{0:8.3f} {1:8.3f} xlo xhi\n".format(0, self.pdb.cell[0]))
            data.write("{0:8.3f} {1:8.3f} ylo yhi\n".format(0, self.pdb.cell[1]))
            data.write("{0:8.3f} {1:8.3f} zlo zhi\n".format(0, self.pdb.cell[2]))
            data.write("\n")
            data.write("Atoms\n")
            data.write("\n")
            for i, atom in enumerate(self.pdb.atoms):
                data.write("{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11}\n")
