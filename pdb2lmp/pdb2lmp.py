from pdb2lmp.pdbreader import PDBReader
from pdb2lmp.moldatabase import MolDatabase
from pdb2lmp.atomdatabase import AtomDatabase


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

        self.natoms = Counter(0, 0)

    def collect_types(self):
        atnum = 0
        for mol in self.pdb.molecules:
            if mol.name not in self.moltypes:
                self.moltypes.append(mol.name)
            for atom in self.moldb.molecules[mol.name].atoms.values():
                if atom.type not in self.atomtypes:
                    self.atomtypes.append(atom.type)
                    self.natoms.types += 1
                if self.pdb.atoms[atnum].name != atom.name:
                    raise NonMatchingAtomException("Atom in PDB ({0}) does not match atom in force field ({1}).".
                                                   format(self.pdb.atoms[atnum].name, atom.name))
                self.natoms.total += 1
                atnum += 1

    def populate_pdb_data(self):
        for atom in self.pdb.atoms:
            atom.populate(self.moldb.molecules[atom.resname].atoms[atom.name])

    def write_data(self, filename):
        with open(filename, "w") as data:
            data.write("LAMMPS 'data.' input file created by PDB2LMP\n")
            data.write("\n")
            data.write("{0:8d} atoms\n".format(self.natoms.total))
            data.write("{0:8d} bonds\n".format(0))
            data.write("{0:8d} angles\n".format(0))
            data.write("{0:8d} dihedrals\n".format(0))
            data.write("{0:8d} impropers\n".format(0))
            data.write("\n")
            data.write("{0:8d} atom types\n".format(self.natoms.types))
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
                data.write("{0:6d} {1:4d} {2:8.3f} {3:8.3f} {4:8.3f} {5:4d} {6:5.2f} {7:8.3f} {8:8.3f} {9:8.3f} {10:5.2f} {11:5.2f}\n".format(
                    i+1, self.atomtypes.index(atom.type)+1, atom.x, atom.y, atom.z,
                    atom.resid, atom.charge, 0, 0, 0, 0, 0
                ))

    def write_forcefield(self, filename):
        with open(filename, "w") as ff:
            ff.write("# Forcefield prepared by PDB2LMP\n")
            ff.write("\n")
            # TODO change these to "0.0 1.0 1.0 12.0" - ELBA standard
            ff.write("pair_style lj/sf/dipole/sf 0.0 0.0 0.0 12.0\n")
            ff.write("special_bonds lj/coul 0.0 0.0 0.0\n")

            # TODO bonded styles

            # TODO find out why I need both of these
            ff.write("\n")
            for i, atomtype in enumerate(self.atomtypes):
                ff.write("mass {0:4d} {1:8.3f} # {2}\n".format(
                    i+1, self.atomdb.atoms[atomtype].mass, atomtype
                ))

            ff.write("\n")
            for i, atomtype in enumerate(self.atomtypes):
                ff.write("set type {0:4d} mass {1:8.3f} # {2}\n".format(
                        i+1, self.atomdb.atoms[atomtype].mass, atomtype
                ))

            ff.write("\n")
            for i, atomtype in enumerate(self.atomtypes):
                for j, atomtype2 in enumerate(self.atomtypes):
                    if i > j:
                        continue
                    sig, eps = self.atomdb.lj(atomtype, atomtype2)
                    ff.write("pair_coeff {0:4d} {1:4d} {2:6.3f} {3:6.3f} # {4}-{5}\n".format(
                        i+1, j+1, eps, sig, atomtype, atomtype2
                    ))
