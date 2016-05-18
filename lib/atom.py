
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

    def populate(self, other):
        """
        Populate this Atom using values from Atom other, where this Atom is missing data.

        Args:
            other: Another Atom instance

        Returns: Nothing

        """
        for item in self.__slots__:
            self.__setattr__(item, Atom.compare(self.__getattribute__(item),
                                                other.__getattribute__(item)))
