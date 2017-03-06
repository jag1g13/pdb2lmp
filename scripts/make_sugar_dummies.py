#!/usr/bin/env python3

import sys

import mdtraj

gro = mdtraj.load(sys.argv[1])

for i in range(1, 6):
    dummy_index = next(gro.top.atoms_by_name("D{0}".format(i))).index
    carbo_index = next(gro.top.atoms_by_name("C{0}".format(i))).index
    vec = gro.xyz[0][dummy_index] - gro.xyz[0][carbo_index]
    gro.xyz[0][dummy_index] -= 1.5 * vec

gro.save("dummies.gro")