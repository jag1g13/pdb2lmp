import os
from collections import namedtuple

from lib.json import Parser


class BondDatabase:
    def __init__(self, filename=os.path.join("data", "bonds.json")):
        db = Parser(filename)
        Param = namedtuple("Param", ["style", "params"])

        for tipe in ["length", "angle", "dihedral", "improper"]:
            setattr(self, tipe, dict())
            for name, bond in db.bonds[tipe].items():
                style, *params = bond.split()
                getattr(self, tipe)[name] = Param(style, " ".join(params))

