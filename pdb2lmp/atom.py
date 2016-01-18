
class Atom:
    __slots__ = ["name", "type",
                 "resname", "resid",
                 "x", "y", "z",
                 "diameter", "rotmass",
                 "charge", "mass",
                 "sig", "eps",
                 "dipole"]

    def __init__(self, name=None, attype=None,
                 resname=None, resid=None,
                 x=None, y=None, z=None,
                 diameter=None, rotmass=None,
                 charge=None, mass=None,
                 sig=None, eps=None,
                 dipole=None):
        self.name = name
        self.type = attype
        self.resname = resname
        self.resid = resid
        self.x = x
        self.y = y
        self.z = z
        self.diameter = diameter
        self.rotmass = rotmass
        self.charge = charge
        self.mass = mass
        self.sig = sig
        self.eps = eps
        self.dipole = dipole

    @classmethod
    def frompdb(cls, name, resname, resid, x, y, z):
        return cls(name=name, resname=resname, resid=resid, x=x, y=y, z=z)

    @classmethod
    def fromatomdb(cls, attype, mass, charge, sig, eps, dipole, diameter, rotmass):
        return cls(attype=attype, mass=mass, charge=charge,
                   sig=sig, eps=eps, dipole=dipole, diameter=diameter, rotmass=rotmass)

    @classmethod
    def frommoldb(cls, name, attype, charge):
        return cls(name=name, attype=attype, charge=charge)

    @staticmethod
    def compare(val1, val2):
        """
        Compare two values.
        Return the second value if both values are the same or the first value is None.
        Return the first value if the second value is None.
        Raise exception if values are different and neither is None.
        Args:
            val1: First value
            val2: Second value

        Returns: One of the values

        """
        if val1 == val2:
            return val2
        elif val1 is None:
            return val2
        elif val2 is None:
            return val1
        else:
            raise Exception("Values for comparison are different and not None.")
            # print(val1, val2)
            # return val1

    def populate(self, other):
        """
        Populate this Atom using values from Atom other, where this Atom is missing data.

        Args:
            other: Another Atom instance

        Returns: Nothing

        """
        self.name = self.compare(self.name, other.name)
        self.type = self.compare(self.type, other.type)
        self.resname = self.compare(self.resname, other.resname)
        self.resid = self.compare(self.resid, other.resid)
        self.x = self.compare(self.x, other.x)
        self.y = self.compare(self.y, other.y)
        self.z = self.compare(self.z, other.z)
        self.diameter = self.compare(self.diameter, other.diameter)
        self.rotmass = self.compare(self.rotmass, other.rotmass)
        self.charge = self.compare(self.charge, other.charge)
        self.mass = self.compare(self.mass, other.mass)
        self.sig = self.compare(self.sig, other.sig)
        self.eps = self.compare(self.eps, other.eps)
        self.dipole = self.compare(self.dipole, other.dipole)
