
class Atom:
    __slots__ = ["name", "type", "resname", "resid", "x", "y", "z"]

    def __init__(self, name=None, attype=None, resname=None, resid=None, x=None, y=None, z=None):
        self.name = name
        self.type = attype
        self.resname = resname
        self.resid = resid
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def frompdb(cls, name, resname, resid, x, y, z):
        return cls(name, None, resname, resid, x, y, z)

