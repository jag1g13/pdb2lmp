#!/usr/bin/env python3

import sys
import os

from collections import namedtuple, deque
from copy import copy

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


class Gro:
    def __init__(self, filename):
        with open(filename) as fin:
            lines = fin.readlines()

        self.header = lines.pop(0).strip()
        self.natoms = int(lines.pop(0))
        self.box = np.fromiter(map(float, lines.pop().split()), dtype=float)

        self.atoms = []
        for line in lines:
            self.atoms.append(Atom.from_gro_line(line))
        assert len(self.atoms) == self.natoms

    def write(self, filename):
        with open(filename, mode="w") as fout:
            print(self.header, file=fout)
            print(" {0:d}".format(self.natoms), file=fout)
            for atom in self.atoms:
                print(atom.as_gro_line, file=fout)
            print("{0:8.4f}{1:8.4f}{2:8.4f}".format(*self.box), file=fout)

    def renumber(self):
        resid, resid_prev = 0, None
        resname_prev = None
        for i, atom in enumerate(self.atoms, start=1):
            atom.id = i
            if (atom.resid != resid_prev) or (atom.resname != resname_prev):
                resid_prev = atom.resid
                resname_prev = atom.resname
                resid += 1
            atom.resid = resid

        self.natoms = len(self.atoms)

    def insert_atom_before_resid(self, resid, new_atom):
        for insert_point, atom in enumerate(self.atoms):
            if atom.resid == resid:
                break
        self.atoms.insert(insert_point, new_atom)

    def __iter__(self):
        return iter(self.atoms)

    def __reversed__(self):
        return reversed(self.atoms)


def rename_roh(gro):
    resname_next = None
    for atom in reversed(gro):
        if atom.resname == "ROH":
            atom.resname = resname_next
            atom.resid += 1
        else:
            resname_next = atom.resname


def copy_atoms(gro):
    insert_atoms = []

    resname_queue = deque(maxlen=2)
    res_sugar_num_next = None
    for atom in reversed(gro):
        try:
            resname = resname_queue.pop()
        except IndexError:
            resname = None

        print(resname, atom.resname)

        if resname != atom.resname:
            resname_queue.append(atom.resname)
        resname_queue.append(resname)

        try:
            res_sugar_num = int(atom.resname[0])

            if res_sugar_num_next is not None and (res_sugar_num == 6 and atom.name == "C6") or (6 > res_sugar_num > 0 and atom.name == "O{}".format(res_sugar_num)):
                new_atom = copy(atom)
                print()
                print(new_atom)
                new_atom.resname = resname
                new_atom.resid += 1
                print(new_atom)
                insert_atoms.append(new_atom)

            resname = atom.resname
            res_sugar_num_next = int(atom.resname[0])
        except ValueError:
            pass

    for atom in insert_atoms:
        print(new_atom)
        gro.insert_atom_before_resid(atom.resid, atom)


if __name__ == "__main__":
    if "-h" in sys.argv or "--help" in sys.argv:
        print("Takes MD coordinate filename, outputs dummies.gro")
        sys.exit(os.EX_OK)

    gro = Gro(sys.argv[1])
    rename_roh(gro)
    gro.renumber()
    gro.write("potato1.gro")
    copy_atoms(gro)
    gro.renumber()
    gro.write("potato2.gro")

