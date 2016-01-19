import unittest

from lib.atom import Atom


class TestAtom(unittest.TestCase):
    def test_create_atom(self):
        atom = Atom()

    def test_store_atom(self):
        atom = Atom("NamE", "TypE")
        self.assertEqual(atom.name, "NamE")
        self.assertEqual(atom.type, "TypE")

    def test_compare(self):
        self.assertEqual(Atom.compare(1, 1), 1)
        self.assertEqual(Atom.compare(None, 1), 1)
        self.assertEqual(Atom.compare(1, None), 1)
        self.assertEqual(Atom.compare(None, None), None)
        with self.assertRaises(Exception):
            Atom.compare(1, 2)

    def test_atom_populate(self):
        atom1 = Atom.fromatomdb("type", 1, -1, 0.5, -0.5, 0, 1, -1)
        atom2 = Atom.frompdb("name", "resname", 1, 0.5, 0.5, 0.5)
        atom1.populate(atom2)

        self.assertEqual(atom1.name, "name")
        self.assertEqual(atom1.type, "type")
        self.assertEqual(atom1.resname, "resname")
        self.assertEqual(atom1.resid, 1)
        self.assertEqual(atom1.x, 0.5)
        self.assertEqual(atom1.y, 0.5)
        self.assertEqual(atom1.z, 0.5)
        self.assertEqual(atom1.diameter, 1)
        self.assertEqual(atom1.rotmass, -1)
        self.assertEqual(atom1.charge, -1)
        self.assertEqual(atom1.mass, 1)
        self.assertEqual(atom1.sig, 0.5)
        self.assertEqual(atom1.eps, -0.5)
        self.assertEqual(atom1.dipole, 0)


if __name__ == '__main__':
    unittest.main()
