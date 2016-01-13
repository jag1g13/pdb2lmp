
class Atom:
    __slots__ = ["name", "type"]

    def __init__(self, name=None, attype=None):
        self.name = name
        self.type = attype
