
class Atom:
    __slots__ = ["name", "type",
                 "resname", "resid",
                 "x", "y", "z",
                 "diameter", "rotmass",
                 "charge", "mass",
                 "sigma", "epsilon",
                 "dipole"]

    def __init__(self, name=None, type=None,
                 resname=None, resid=None,
                 x=None, y=None, z=None,
                 diameter=None, rotmass=None,
                 charge=None, mass=None,
                 sigma=None, epsilon=None,
                 dipole=None):
        self.name = name
        self.type = type
        self.resname = resname
        self.resid = resid
        self.x = x
        self.y = y
        self.z = z
        self.diameter = diameter
        self.rotmass = rotmass
        self.charge = charge
        self.mass = mass
        self.sigma = sigma
        self.epsilon = epsilon
        self.dipole = dipole

    def __repr__(self):
        return "<Atom name={0}, resname={1}, resnum={2}, type={3}>".format(self.name, self.resname, self.resid, self.type)

    @classmethod
    def frompdb(cls, name, resname, resid, x, y, z):
        return cls(name=name, resname=resname, resid=resid, x=x, y=y, z=z)

    @classmethod
    def from_atom_db(cls, **kwargs):
        if "rotmass" not in kwargs:
            kwargs["rotmass"] = kwargs["mass"]
        return cls(**kwargs)

    @classmethod
    def from_dict(cls, **kwargs):
        return cls(**kwargs)

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
