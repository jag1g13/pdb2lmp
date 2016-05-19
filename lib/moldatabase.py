import os

from collections import OrderedDict

from lib.json import Parser
from lib.atom import Atom


class Molecule:
    __slots__ = ["atoms", "lengths", "angles", "dihedrals", "impropers", "bonds", "polymer_type"]

    def __init__(self, **kwargs):
        self.atoms = OrderedDict()
        self.lengths = []
        self.angles = []
        self.dihedrals = []
        self.impropers = []
        self.polymer_type = set()

        for key, value in kwargs.items():
            try:
                getattr(self, key).extend(value)
            except AttributeError:
                getattr(self, key).update(value)

        self.bonds = self.lengths


class MolDatabase:
    def __init__(self, filename=os.path.join("data", "mol-elba.json")):
        """
        Create a new MolDatabase object

        Args:
            filename: Name of molecule database file to open.
        """
        db = Parser(filename)
        self.version = db.version
        self.molecules = {}

        for name, data in db.molecules.items():
            atoms = data.pop("atoms")
            self.molecules[name] = Molecule(**data)
            for atom in atoms:
                self.molecules[name].atoms[atom.name] = Atom.from_dict(**atom)
