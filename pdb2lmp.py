#!/usr/bin/env python3

import argparse
import os

from lib.coordreaders import PDBReader, GROReader
from lib.moldatabase import MolDatabase
from lib.atomdatabase import AtomDatabase
from lib.bonddatabase import BondDatabase


class NonMatchingAtomException(Exception):
    def __init__(self, num, name1, name2):
        line = "Atom {0} in coordinate file ({1}) does not match atom in force field ({2})."
        super(NonMatchingAtomException, self).__init__(line.format(num, name1, name2))


class PolymerError(Exception):
    def __init__(self, name1, name2):
        line = "Molecules {0} and {1} do not have matching polymer types"
        super(PolymerError, self).__init__(line.format(name1, name2))


class Counter:
    __slots__ = ["total", "types"]

    def __init__(self, total=0, types=0):
        self.total = total
        self.types = types

    def __repr__(self):
        return "<Counter: (total={0}, types={1})>".format(self.total, self.types)


class PDB2LMP:
    def __init__(self, infile):
        self._suppress_atom_names = False

        formats = {"pdb": PDBReader,
                   "gro": GROReader}
        coords = formats[os.path.splitext(infile)[1][1:]](infile)

        self.coords = coords
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

        self.natoms = Counter()
        self.nlengths = Counter()
        self.nangles = Counter()
        self.ndihedrals = Counter()
        self.nimpropers = Counter()

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

        for mol in self.coords.molecules:
            dbmol = self.moldb.molecules[mol.name]

            if mol.name not in self.moltypes:
                self.moltypes.append(mol.name)

                collect_type(dbmol.lengths, self.nlengths, self.bonddb.length,
                             self.lentypes, self.lenstyles)
                collect_type(dbmol.angles, self.nangles, self.bonddb.angle,
                             self.angtypes, self.angstyles)
                collect_type(dbmol.dihedrals, self.ndihedrals, self.bonddb.dihedral,
                             self.dihtypes, self.dihstyles)
                collect_type(dbmol.impropers, self.nimpropers, self.bonddb.improper,
                             self.imptypes, self.impstyles)

            coordfile_atoms = [self.coords.atoms[x] for x in mol.atoms]
            if len(coordfile_atoms) != len(dbmol.atoms):
                raise ValueError("Number of atoms does not match between coordinate file and force field for molecule {0}.".format(mol.name))

            for coordfile_atom, dbmol_atom in zip(coordfile_atoms, dbmol.atoms.values()):
                if dbmol_atom.type not in self.atomtypes:
                    self.atomtypes.append(dbmol_atom.type)
                    self.natoms.types += 1

                if coordfile_atom.name != dbmol_atom.name:
                    if self._suppress_atom_names:
                            coordfile_atom.name = dbmol_atom.name
                    else:
                        raise NonMatchingAtomException(atnum, coordfile_atom.name, dbmol_atom.name)
                self.natoms.total += 1
                atnum += 1

    def populate_pdb_data(self):
        for mol in self.moldb.molecules.values():
            for atom in mol.atoms.values():
                atom.populate(self.atomdb.atoms[atom.type])
        for atom in self.coords.atoms:
            atom.populate(self.moldb.molecules[atom.resname].atoms[atom.name])

    def write_data(self, filename):
        with open(filename, "w") as data:
            print("LAMMPS 'data.' input file created by PDB2LMP", file=data)
            print(file=data)
            print("{0:8d} atoms".format(self.natoms.total), file=data)
            print("{0:8d} bonds".format(self.nlengths.total), file=data)
            print("{0:8d} angles".format(self.nangles.total), file=data)
            print("{0:8d} dihedrals".format(self.ndihedrals.total), file=data)
            print("{0:8d} impropers".format(self.nimpropers.total), file=data)
            print(file=data)
            print("{0:8d} atom types".format(self.natoms.types), file=data)
            print("{0:8d} bond types".format(self.nlengths.types), file=data)
            print("{0:8d} angle types".format(self.nangles.types), file=data)
            print("{0:8d} dihedral types".format(self.ndihedrals.types), file=data)
            print("{0:8d} improper types".format(self.nimpropers.types), file=data)
            print(file=data)
            cell = [val / 2 for val in self.coords.cell]
            print("{0:8.3f} {1:8.3f} xlo xhi".format(-cell[0], cell[0]), file=data)
            print("{0:8.3f} {1:8.3f} ylo yhi".format(-cell[1], cell[1]), file=data)
            print("{0:8.3f} {1:8.3f} zlo zhi".format(-cell[2], cell[2]), file=data)
            print(file=data)
            print("Atoms", file=data)
            print(file=data)

            atomline = "{0:6d} {1:4d} {2:8.3f} {3:8.3f} {4:8.3f} {5:4d} {6:5.2f} {7:8.3f} {8:8.3f} {9:8.3f} {10:5.2f} {11:5.2f}"
            for i, atom in enumerate(self.coords.atoms, start=1):
                # Write atom line
                # Dipoles are all oriented up - this should equilibrate out quickly
                print(atomline.format(i, self.atomtypes.index(atom.type)+1,
                                      atom.x, atom.y, atom.z, atom.resid, atom.charge,
                                      atom.dipole, 0, 0, atom.diameter, atom.rotmass), file=data)

            def write_bonds(n, types, header):
                if n <= 0:
                    return
                print("\n" + header + "\n", file=data)
                i = 1
                for ii, mol in enumerate(self.coords.molecules):
                    mol_db = self.moldb.molecules[mol.name]
                    atom_list = list(mol_db.atoms.keys())
                    for bond in getattr(mol_db, header.lower()):
                        print("{0:6d} {1:4d}".format(i, types.index(bond.type) + 1), file=data, end="")
                        for atom in bond.atoms:
                            try:
                                atom_num = mol.atoms[atom_list.index(atom)]
                            except ValueError:
                                if atom.startswith("+"):
                                    other_mol = self.coords.molecules[ii + 1]
                                elif atom.startswith("-"):
                                    other_mol = self.coords.molecules[ii - 1]
                                else:
                                    raise

                                other_mol_db = self.moldb.molecules[other_mol.name]
                                try:
                                    if not mol_db.polymer_type.intersection(other_mol_db.polymer_type):
                                        raise PolymerError(mol.name, other_mol.name) from None
                                except AttributeError:
                                    raise PolymerError(mol.name, other_mol.name) from None

                                other_atom_list = list(other_mol_db.atoms.keys())
                                atom_num = other_mol.atoms[other_atom_list.index(atom[1:])]

                            print(" {0:6d}".format(atom_num + 1), file=data, end="")
                        print(file=data)
                        i += 1

            write_bonds(self.nlengths.total, self.lentypes, "Bonds")
            write_bonds(self.nangles.total, self.angtypes, "Angles")
            write_bonds(self.ndihedrals.total, self.dihtypes, "Dihedrals")
            write_bonds(self.nimpropers.total, self.imptypes, "Impropers")

    def write_forcefield(self, filename):
        with open(filename, "w") as ff:
            print("# Forcefield prepared by PDB2LMP", file=ff)
            print(file=ff)
            # TODO change these to "0.0 1.0 1.0 12.0" - ELBA standard
            print("pair_style lj/sf/dipole/sf 12.0", file=ff)
            print("special_bonds lj/coul 0.0 0.0 0.0", file=ff)
            print(file=ff)

            def write_styles(styles, header):
                if styles:
                    print(header, file=ff, end="")
                    for style in styles:
                        print(" " + style, file=ff, end="")
                    print(file=ff)

            write_styles(self.lenstyles, "bond_style hybrid")
            write_styles(self.angstyles, "angle_style hybrid")
            write_styles(self.dihstyles, "dihedral_style hybrid")
            write_styles(self.impstyles, "improper_style hybrid")

            print(file=ff)
            line = "mass {0:4d} {1:8.3f} # {2}"
            for i, atomtype in enumerate(self.atomtypes, start=1):
                print(line.format(i, self.atomdb.atoms[atomtype].mass, atomtype), file=ff)

            print(file=ff)
            line = "set type{0:4d} diameter {1:8.3f} # {2}"
            for i, atomtype in enumerate(self.atomtypes, start=1):
                print(line.format(i, self.atomdb.atoms[atomtype].diameter, atomtype), file=ff)

            print(file=ff)
            line = "pair_coeff {0:4d} {1:4d} {2:6.3f} {3:6.3f} # {4}-{5}"
            for i, atomtype in enumerate(self.atomtypes, start=1):
                for j, atomtype2 in enumerate(self.atomtypes, start=1):
                    if i > j:
                        continue
                    sig, eps = self.atomdb.lj(atomtype, atomtype2)
                    print(line.format(i, j, eps, sig, atomtype, atomtype2), file=ff)

            def write_types(types, db_vals, line_prefix):
                if types:
                    print(file=ff)
                    line = line_prefix + " {0:4d} {1} {2} # {3}"
                    for i, tipe in enumerate(types, start=1):
                        db_type = db_vals[tipe]
                        print(line.format(i, db_type.style, db_type.params, tipe), file=ff)

            write_types(self.lentypes, self.bonddb.length, "bond_coeff")
            write_types(self.angtypes, self.bonddb.angle, "angle_coeff")
            write_types(self.dihtypes, self.bonddb.dihedral, "dihedral_coeff")
            write_types(self.imptypes, self.bonddb.improper, "improper_coeff")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDB/GRO into LAMMPS input files.")
    parser.add_argument("infile", type=str,
                        help="PDB/GRO to convert")
    parser.add_argument("outfiles", type=str, default="out",
                        help="output filenames")
    args = parser.parse_args()

    conv = PDB2LMP(args.infile)
    conv.collect_types()
    conv.populate_pdb_data()
    conv.write_data(args.outfiles + ".data")
    conv.write_forcefield(args.outfiles + ".ff")
