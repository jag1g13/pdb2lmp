#!/usr/bin/env python3

import sys
import os

from collections import namedtuple
from copy import deepcopy

import numpy as np

FormatSpec = namedtuple("FormatSpec", ["type", "slice"])


class Atom:
    def __init__(self, resid=None, resname=None, name=None,
                 id=None, x=None, y=None, z=None):
        self.resid = resid
        self.resname = resname
        self.name = name
        self.id = id
        self.coords = np.array([x, y, z])

    def __repr__(self):
        return "<Atom {0}: '{1}' in {2}: '{3}'>".format(self.id, self.name, self.resid, self.resname)

    @classmethod
    def from_gro_line(cls, line):
        slices = {
            "resid":   FormatSpec(int, slice( 0,  5)),
            "resname": FormatSpec(str, slice( 5, 10)),
            "name":    FormatSpec(str, slice(10, 15)),
            "id":      FormatSpec(int, slice(15, 20)),
            "x":       FormatSpec(float, slice(20, 28)),
            "y":       FormatSpec(float, slice(28, 36)),
            "z":       FormatSpec(float, slice(36, 44))
        }
        return cls(**{k: (line[v.slice].strip() if v.type == str else v.type(line[v.slice])) for k, v in slices.items()})

    @property
    def as_gro_line(self):
        return "{0:5d}{1:5s}{2:>5s}{3:5d}{4:8.3f}{5:8.3f}{6:8.3f}".format(self.resid, self.resname, self.name,
                                                                               self.id, *self.coords)


class Residue:
    def __init__(self, resid, resname):
        self.resid = resid
        self.resname = resname
        self.atoms = []

    @property
    def natoms(self):
        return len(self.atoms)

    @property
    def is_sugar(self):
        try:
            int(self.resname[0])
            return True
        except ValueError:
            return False

    @property
    def is_water(self):
        return self.resname in {"WAT", "SOL", "HOH"}

    def atom_by_name(self, name):
        for atom in self.atoms:
            if atom.name == name:
                return atom
        raise ValueError("Atom {} not in Residue {}".format(name, self.resname))

    def add_atom(self, atom, left=False):
        atom.resid = self.resid
        atom.resname = self.resname

        if left:
            self.atoms.insert(0, atom)
        else:
            self.atoms.append(atom)

    def __iter__(self):
        return iter(self.atoms)


class Gro:
    def __init__(self, filename):
        with open(filename) as fin:
            lines = fin.readlines()

        self.header = lines.pop(0).strip()
        self.natoms = int(lines.pop(0))
        self.box = np.fromiter(map(float, lines.pop().split()), dtype=float)

        self.residues = []
        resid_last = None
        for line in lines:
            atom = Atom.from_gro_line(line)
            if atom.resid != resid_last:
                self.residues.append(Residue(atom.resid, atom.resname))
                resid_last = atom.resid
            self.residues[-1].add_atom(atom)

        assert sum(x.natoms for x in self.residues) == self.natoms

    def write(self, filename):
        with open(filename, mode="w") as fout:
            print(self.header, file=fout)
            print(" {0:d}".format(self.natoms), file=fout)
            for residue in self.residues:
                for atom in residue:
                    print(atom.as_gro_line, file=fout)
            print("{0:10.4f}{1:10.4f}{2:10.4f}".format(*self.box), file=fout)

    def renumber(self):
        atom_id = 0
        for i, residue in enumerate(self.residues, start=1):
            residue.resid = i
            for atom in residue:
                atom.resid = i
                atom_id += 1
                atom.id = atom_id

        self.natoms = sum(x.natoms for x in self.residues)

    def prepend_atoms_to_residue(self, resid, atoms):
        try:
            for atom in reversed(atoms):
                self.residues[resid].add_atom(atom, left=True)
        except TypeError:
            self.residues[resid].add_atom(atom, left=True)

        self.renumber()


def rename_roh(gro):
    to_delete = []
    for i, residue in enumerate(gro.residues):
        if residue.resname == "ROH":
            atoms = residue.atoms
            gro.prepend_atoms_to_residue(i+1, atoms)
            to_delete.append(i)

    for offset, resid in enumerate(to_delete):
        gro.residues.pop(resid - offset)

    gro.renumber()


def copy_link_atoms(gro):
    for i, residue in enumerate(gro.residues):
        try:
            res_sugar_num = int(residue.resname[0])
            res_next = gro.residues[i+1]
            int(res_next.resname[0])
        except ValueError:
            continue

        for atom in residue:
            if (res_sugar_num == 6 and atom.name == "C6") or (6 > res_sugar_num > 0 and atom.name == "O{}".format(res_sugar_num)):
                new_atom = deepcopy(atom)
                new_atom.name = "O1"
                res_next.add_atom(new_atom, left=True)

    gro.renumber()


def prune_atoms(gro):
    keep_names = {"C1", "C2", "C3", "C4", "C5", "O5", "O1", "O2", "O3", "O4", "C6"}
    for residue in gro.residues:
        if residue.is_sugar:
            residue.atoms = [atom for atom in residue if atom.name in keep_names]
        elif residue.is_water:
            residue.atoms = [atom for atom in residue if atom.name in {"O", "O1", "OW"}]
    gro.renumber()


def rename_dummies(gro):
    dummy_names = {
        "O1": "D1",
        "O2": "D2",
        "O3": "D3",
        "O4": "D4",
        "C6": "D5"
    }
    for residue in gro.residues:
        if residue.is_sugar:
            for atom in residue:
                if atom.name in dummy_names:
                    atom.name = dummy_names[atom.name]
        elif residue.is_water:
            residue.atoms[0].name = "O1"


def sort_atoms(gro):
    order = ["C1", "C2", "C3", "C4", "C5", "O5", "D1", "D2", "D3", "D4", "D5"]
    for residue in gro.residues:
        if residue.is_sugar:
            residue.atoms = sorted(residue.atoms, key=lambda x: order.index(x.name))
    gro.renumber()


def move_dummies(gro):
    for residue in gro.residues:
        if residue.is_sugar:
            for i in range(1, 6):
                vec = residue.atom_by_name("D{}".format(i)).coords - residue.atom_by_name("C{}".format(i)).coords
                residue.atom_by_name("D{}".format(i)).coords -= 1.5 * vec
                print("D{}".format(i))
                print(np.sum(vec*vec))


if __name__ == "__main__":
    if "-h" in sys.argv or "--help" in sys.argv:
        print("Takes MD coordinate filename, outputs dummies.gro")
        sys.exit(os.EX_OK)

    gro = Gro(sys.argv[1])

    rename_roh(gro)
    copy_link_atoms(gro)
    prune_atoms(gro)
    rename_dummies(gro)
    sort_atoms(gro)
    move_dummies(gro)

    gro.write("dummies.gro")

