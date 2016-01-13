from collections import namedtuple

from ..pdb2lmp.pdbreader import PDBReader
from ..pdb2lmp.moldatabase import MolDatabase
from ..pdb2lmp.atomdatabase import AtomDatabase

class PDB2LMP:
    def __init__(self, pdbname):
        self.pdb = PDBReader(pdbname)
        self.moldb = MolDatabase()
        self.atomdb = AtomDatabase()

        self.moltypes = []
        self.atomtypes = []

    def collect_types(self):
        Counter = namedtuple("Counter", ["total", "types"])

        for mol in self.pdb.molecules:
            if mol.name not in self.moltypes:
                self.moltypes.append(mol.name)
                for atomname, atom in self.moldb.molecules[mol.name].atoms.items():
                    if atom.type not in self.atomtypes:
                        self.atomtypes.append(atom.type)

        self.atoms = Counter(self.pdb.natoms, len(self.atomtypes))

    def write_data(self, filename):
        with open(filename, "w") as data:
            data.write("LAMMPS 'data.' input file created by PDB2LMP\n")
            data.write("\n")
            data.write("{0} atoms\n".format(self.atoms.total))
            data.write("{0} bonds\n".format(0))
            data.write("{0} angles\n".format(0))
            data.write("{0} dihedrals\n".format(0))
            data.write("{0} impropers\n".format(0))
            data.write("\n")
            data.write("{0} atom types\n".format(self.atoms.types))
            data.write("{0} bond types\n".format(0))
            data.write("{0} angle types\n".format(0))
            data.write("{0} dihedral types\n".format(0))
            data.write("{0} improper types\n".format(0))
            data.write("\n")
