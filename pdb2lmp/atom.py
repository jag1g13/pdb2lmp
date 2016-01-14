
class Atom:
    __slots__ = ["name", "type",
                 "resname", "resid",
                 "x", "y", "z",
                 "diameter", "rotmass",
                 "charge", "mass",
                 "sig", "eps"]

    def __init__(self, name=None, attype=None, resname=None, resid=None,
                 x=None, y=None, z=None, charge=None, mass=None,
                 sig=None, eps=None):
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
        self.mass = mass
        self.sig = sig
        self.eps = eps

    @classmethod
    def frompdb(cls, name, resname, resid, x, y, z):
        return cls(name=name, resname=resname, resid=resid, x=x, y=y, z=z)

    @classmethod
    def fromdb(cls, attype, mass, charge, sig, eps):
        return cls(attype=attype, mass=mass, charge=charge, sig=sig, eps=eps)

