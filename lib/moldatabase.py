import os

from collections import OrderedDict

from lib.json import Parser
from lib.atom import Atom


class Molecule:
    __slots__ = ["atoms", "lengths", "angles", "dihedrals",
                 "impropers", "bonds", "polymer_type", "templates"]

    def __init__(self, **kwargs):
        self.atoms = OrderedDict()
        self.lengths = []
        self.angles = []
        self.dihedrals = []
        self.impropers = []
        self.polymer_type = set()
        self.templates = set()

        for key, value in kwargs.items():
            try:
                getattr(self, key).extend(value)
            except AttributeError:
                getattr(self, key).update(value)

        self.bonds = self.lengths

    def extend(self, mol):
        for key in self.__slots__:
            if key == "bonds":
                continue
            try:
                getattr(self, key).extend(getattr(mol, key))
            except AttributeError:
                getattr(self, key).update(getattr(mol, key))


class MolDatabase:
    def __init__(self, filename=None):
        """
        Create a new MolDatabase object

        Args:
            filename: Name of molecule database file to open.
        """
        if filename is None:
            filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                    os.path.join("data", "mol-elba.json"))

        db = Parser(filename)
        try:
            self.version = db.version
        except KeyError:
            self.version = None
        self.molecules = {}

        for name, data in db.molecules.items():
            try:
                # Pop this because we want to add it separately
                atoms = data.pop("atoms")
            except KeyError:
                atoms = []
            self.molecules[name] = Molecule(**data)
            for atom in atoms:
                self.molecules[name].atoms[atom.name] = Atom(**atom)

        for mol in self.molecules.values():
            for template in mol.templates:
                mol.extend(self.molecules[template])
