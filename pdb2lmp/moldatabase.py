import os

from collections import OrderedDict, namedtuple


class MolDatabase:
    data_dir = "data"

    def __init__(self, filename):
        """
        Create a new MolDatabase object

        Args:
            filename: Name of molecule database file to open; GROMACS rtp file.
        """
        with open(os.path.join(MolDatabase.data_dir, filename)) as f:
            current_mol = None
            self.molecules = {}
            Atom = namedtuple("Atom", ["name", "type", "charge"])
            Molecule = namedtuple("Molecule", ["name", "atoms", "bonds", "angles", "dihedrals", "impropers"])

            for line in f:
                line = line.strip()
                toks = line.split()
                if toks[0] in {"#", ";"}:
                    continue
                if toks[0] == "[":
                    if toks[1] not in {"atoms", "bonds", "angles", "dihedrals", "impropers"}:
                        current_mol = toks[1]
                        self.molecules[current_mol] = Molecule(current_mol, OrderedDict(), set(), set(), set(), set())
                    elif current_mol is not None:
                        current_mode = toks[1]
                    assert toks[2] == "]"
                else:
                    if current_mode == "atoms":
                        self.molecules[current_mol].atoms[toks[0]] = Atom(toks[0], toks[1], float(toks[2]))
