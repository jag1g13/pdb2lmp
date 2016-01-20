import argparse

from lib.pdbreader import PDBReader
from lib.moldatabase import MolDatabase
from lib.atomdatabase import AtomDatabase
from lib.bonddatabase import BondDatabase


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
        self.bonddb = BondDatabase()

        self.moltypes = []
        self.atomtypes = []
        self.lengthtypes = []
        self.angtypes = []
        self.dihtypes = []
        self.imptypes = []

        self.natoms = Counter(0, 0)
        self.nlengths = Counter(0, 0)
        self.nangles = Counter(0, 0)
        self.ndihedrals = Counter(0, 0)
        self.nimpropers = Counter(0, 0)

    def collect_types(self):
        atnum = 0
        for mol in self.pdb.molecules:

            if mol.name not in self.moltypes:
                self.moltypes.append(mol.name)

                for lentype in self.moldb.molecules[mol.name].lengths:
                    self.nlengths.total += 1
                    if lentype.type not in self.lengthtypes:
                        self.lengthtypes.append(lentype.type)
                        self.nlengths.types += 1

                for angtype in self.moldb.molecules[mol.name].angles:
                    self.nangles.total += 1
                    if angtype.type not in self.angtypes:
                        self.angtypes.append(angtype.type)
                        self.nangles.types += 1

                for dihtype in self.moldb.molecules[mol.name].dihedrals:
                    self.ndihedrals.total += 1
                    if dihtype.type not in self.dihtypes:
                        self.dihtypes.append(dihtype.type)
                        self.ndihedrals.types += 1

                for imptype in self.moldb.molecules[mol.name].impropers:
                    self.nimpropers.total += 1
                    if imptype.type not in self.imptypes:
                        self.imptypes.append(imptype.type)
                        self.nimpropers.types += 1

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
        for mol in self.moldb.molecules.values():
            for atom in mol.atoms.values():
                atom.populate(self.atomdb.atoms[atom.type])
        for atom in self.pdb.atoms:
            atom.populate(self.moldb.molecules[atom.resname].atoms[atom.name])

    def write_data(self, filename):
        with open(filename, "w") as data:
            data.write("LAMMPS 'data.' input file created by PDB2LMP\n")
            data.write("\n")
            data.write("{0:8d} atoms\n".format(self.natoms.total))
            data.write("{0:8d} bonds\n".format(self.nlengths.total))
            data.write("{0:8d} angles\n".format(self.nangles.total))
            data.write("{0:8d} dihedrals\n".format(self.ndihedrals.total))
            data.write("{0:8d} impropers\n".format(self.nimpropers.total))
            data.write("\n")
            data.write("{0:8d} atom types\n".format(self.natoms.types))
            data.write("{0:8d} bond types\n".format(self.nangles.types))
            data.write("{0:8d} angle types\n".format(self.nangles.types))
            data.write("{0:8d} dihedral types\n".format(self.ndihedrals.types))
            data.write("{0:8d} improper types\n".format(self.nimpropers.types))
            data.write("\n")
            data.write("{0:8.3f} {1:8.3f} xlo xhi\n".format(0, self.pdb.cell[0]))
            data.write("{0:8.3f} {1:8.3f} ylo yhi\n".format(0, self.pdb.cell[1]))
            data.write("{0:8.3f} {1:8.3f} zlo zhi\n".format(0, self.pdb.cell[2]))
            data.write("\n")
            data.write("Atoms\n")
            data.write("\n")
            for i, atom in enumerate(self.pdb.atoms):
                # Write atom line
                # Dipoles are all oriented up - this should equilibrate out quickly
                data.write("{0:6d} {1:4d} {2:8.3f} {3:8.3f} {4:8.3f} {5:4d} {6:5.2f} {7:8.3f} {8:8.3f} {9:8.3f} {10:5.2f} {11:5.2f}\n".format(
                    i+1, self.atomtypes.index(atom.type)+1, atom.x, atom.y, atom.z,
                    atom.resid, atom.charge, atom.dipole, 0, 0, atom.diameter, atom.rotmass
                ))

            data.write("\n")
            data.write("Bonds\n")
            data.write("\n")
            i = 0
            for mol in self.pdb.molecules:
                for length in self.moldb.molecules[mol.name].lengths:
                    data.write("{0:6d} {1:4d} {2:6d} {3:6d}\n".format(
                        i+1, self.lengthtypes.index(length.type)+1,
                        mol.atoms[list(self.moldb.molecules[mol.name].atoms.keys()).index(length.atom1)]+1,
                        mol.atoms[list(self.moldb.molecules[mol.name].atoms.keys()).index(length.atom2)]+1
                    ))
                    i += 1

            data.write("\n")
            data.write("Angles\n")
            data.write("\n")
            i = 0
            for mol in self.pdb.molecules:
                for angle in self.moldb.molecules[mol.name].angles:
                    data.write("{0:6d} {1:4d} {2:6d} {3:6d} {4:6d}\n".format(
                            i+1, self.angtypes.index(angle.type)+1,
                            mol.atoms[list(self.moldb.molecules[mol.name].atoms.keys()).index(angle.atom1)]+1,
                            mol.atoms[list(self.moldb.molecules[mol.name].atoms.keys()).index(angle.atom2)]+1,
                            mol.atoms[list(self.moldb.molecules[mol.name].atoms.keys()).index(angle.atom3)]+1
                    ))
                    i += 1

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
                ff.write("set type {0:4d} diameter {1:8.3f} # {2}\n".format(
                        i+1, self.atomdb.atoms[atomtype].diameter, atomtype
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

            ff.write("\n")
            for i, lentype in enumerate(self.lengthtypes):
                ff.write("bond_coeff {0:4d} {1} # {2}\n".format(
                    i+1, self.bonddb.lengths[lentype], lentype))

            ff.write("\n")
            for i, angtype in enumerate(self.angtypes):
                ff.write("angle_coeff {0:4d} {1} # {2}\n".format(
                        i+1, self.bonddb.angles[angtype], angtype))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDB into LAMMPS input files.")
    parser.add_argument("pdb", type=str,
                        help="PDB to convert")
    parser.add_argument("out", type=str, default="out",
                        help="output filenames")
    args = parser.parse_args()
    conv = PDB2LMP(args.pdb)
    conv.collect_types()
    conv.populate_pdb_data()
    conv.write_data(args.out + ".data")
    conv.write_forcefield(args.out + ".ff")
