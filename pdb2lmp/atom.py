
class Atom:
    __slots__ = ["name", "type", "resname", "resid", "x", "y", "z", "diameter", "rotmass", "charge"]

    def __init__(self, name=None, attype=None, resname=None, resid=None, x=None, y=None, z=None):
        self.name = name
        self.type = attype
        self.resname = resname
        self.resid = resid
        self.x = x
        self.y = y
        self.z = z
        self.diameter = -1
        self.rotmass = -1
        self.charge = -1

    @classmethod
    def frompdb(cls, name, resname, resid, x, y, z):
        return cls(name, None, resname, resid, x, y, z)

