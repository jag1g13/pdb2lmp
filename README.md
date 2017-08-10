[![Build Status](https://travis-ci.org/jag1g13/pdb2lmp.svg?branch=master)](https://travis-ci.org/jag1g13/pycgtool)

# pdb2lmp
Convert PDB files to LAMMPS data and force field files.
Requires Python 3.4 or greater.

## Aim
This program uses a library of pre-defined molecule, atom, and bond types to convert PDB or GRO files into LAMMPS input DATA (topology) and FF (forcefield) files.  It was inspired by the GROMACS tool PDB2GMX as an attempt to make it easier to setup simulations using the [ELBA forcefield](https://github.com/orsim/elba-lammps).  It should however be more broadly applicable to molecular simulation in LAMMPS in general.

## Use
To use the program, execute:

`python pdb2lmp.py <PDB/GRO input> <output name>`

e.g.:

`python pdb2lmp.py data/water.pdb water`

Output DATA and FF files are created using the output name specified appended with the prefixes `.data` and `.ff` respectively.  For the conversion to be successful the molecule names in the import PDB/GRO must match an entry in the PDB2LMP molecule file.  If a molecule is missing it may be added to `data/mol-elba.json`.
