
class Atom:
    __slots__ = ["name", "type", "resname", "resid", "x", "y", "z",
                 "diameter", "rotmass", "charge", "mass",
                 "sigma", "epsilon", "dipole"]

    def __init__(self, **kwargs):
        for key in self.__slots__:
            try:
                setattr(self, key, kwargs[key])
            except KeyError:
                setattr(self, key, None)

    def __repr__(self):
        line = "<Atom name={0}, resname={1}, resnum={2}, type={3}>"
        return line.format(self.name, self.resname, self.resid, self.type)

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
            raise ValueError("Values for comparison are different and not None.")

    def populate(self, other):
        """
        Populate this Atom using values from Atom other, where this Atom is missing data.

        Args:
            other: Another Atom instance

        Returns: Nothing

        """
        for key in self.__slots__:
            val = Atom.compare(getattr(self, key), getattr(other, key))
            setattr(self, key, val)
