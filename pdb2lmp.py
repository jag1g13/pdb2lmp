#!/usr/bin/env python

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
        self.lentypes = []
        self.angtypes = []
        self.dihtypes = []
        self.imptypes = []

        self.lenstyles = []
        self.angstyles = []
        self.dihstyles = []
        self.impstyles = []

        self.natoms = Counter(0, 0)
        self.nlengths = Counter(0, 0)
        self.nangles = Counter(0, 0)
        self.ndihedrals = Counter(0, 0)
        self.nimpropers = Counter(0, 0)

    def collect_types(self):

        def collect_type(values, counter, db_vals, typelist, stylelist):
            for val in values:
                counter.total += 1
                if val.type not in typelist:
                    typelist.append(val.type)
                    counter.types += 1
                    if db_vals[val.type].style not in stylelist:
                        stylelist.append(db_vals[val.type].style)

        atnum = 0

        for mol in self.pdb.molecules:
            dbmol = self.moldb.molecules[mol.name]

            if mol.name not in self.moltypes:
                self.moltypes.append(mol.name)

                collect_type(dbmol.lengths, self.nlengths, self.bonddb.lengths,
                             self.lentypes, self.lenstyles)
                collect_type(dbmol.angles, self.nangles, self.bonddb.angles,
                             self.angtypes, self.angstyles)
                collect_type(dbmol.dihedrals, self.ndihedrals, self.bonddb.dihedrals,
                             self.dihtypes, self.dihstyles)
                collect_type(dbmol.impropers, self.nimpropers, self.bonddb.impropers,
                             self.imptypes, self.impstyles)

            for atom in dbmol.atoms.values():
                if atom.type not in self.atomtypes:
                    self.atomtypes.append(atom.type)
                    self.natoms.types += 1
                if self.pdb.atoms[atnum].name != atom.name:
                    raise NonMatchingAtomException("Atom {0} in PDB ({1}) does not match atom in force field ({2}).".
                                                   format(atnum, self.pdb.atoms[atnum].name, atom.name))
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

            def write_bonds(n, types, header):
                if n <= 0:
                    return
                data.write("\n" + header + "\n\n")
                i = 0
                for mol in self.pdb.molecules:
                    atom_list = list(self.moldb.molecules[mol.name].atoms.keys())
                    for bond in getattr(self.moldb.molecules[mol.name], header.lower()):
                        data.write("{0:6d} {1:4d}".format(i+1, types.index(bond.type) + 1))
                        for atom in bond.atoms:
                            data.write(" {0:6d}".format(mol.atoms[atom_list.index(atom)] + 1))
                        data.write("\n")
                        i += 1

            write_bonds(self.nlengths.total, self.lentypes, "Bonds")
            write_bonds(self.nangles.total, self.angtypes, "Angles")
            write_bonds(self.ndihedrals.total, self.dihtypes, "Dihedrals")
            write_bonds(self.nimpropers.total, self.imptypes, "Impropers")

    def write_forcefield(self, filename):
        with open(filename, "w") as ff:
            ff.write("# Forcefield prepared by PDB2LMP\n")
            ff.write("\n")
            # TODO change these to "0.0 1.0 1.0 12.0" - ELBA standard
            ff.write("pair_style lj/sf/dipole/sf 0.0 0.0 0.0 12.0\n")
            ff.write("special_bonds lj/coul 0.0 0.0 0.0\n")

            def write_styles(styles, header):
                if styles is not []:
                    ff.write(header)
                    for style in styles:
                        ff.write(" " + style)
                    ff.write("\n")

            write_styles(self.lenstyles, "bond_style hybrid")
            write_styles(self.angstyles, "angle_style hybrid")
            write_styles(self.dihstyles, "dihedral_style hybrid")
            write_styles(self.impstyles, "improper_style hybrid")

            ff.write("\n")
            for i, atomtype in enumerate(self.atomtypes):
                ff.write("mass {0:4d} {1:8.3f} # {2}\n".format(
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

            def write_types(types, db_vals, line_prefix):
                if types is not []:
                    ff.write("\n")
                    for i, tipe in enumerate(types):
                        ff.write(line_prefix + " {0:4d} {1} {2} # {3}\n".format(
                            i+1, db_vals[tipe].style, db_vals[tipe].params, tipe))

            write_types(self.lentypes, self.bonddb.lengths, "bond_coeff")
            write_types(self.angtypes, self.bonddb.angles, "angle_coeff")
            write_types(self.dihtypes, self.bonddb.dihedrals, "dihedral_coeff")
            write_types(self.imptypes, self.bonddb.impropers, "improper_coeff")

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
