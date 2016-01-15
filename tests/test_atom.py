import unittest

from pdb2lmp.atom import Atom


class TestAtom(unittest.TestCase):
    def test_create_atom(self):
        atom = Atom()

    def test_store_atom(self):
        atom = Atom("NamE", "TypE")
        self.assertEqual(atom.name, "NamE")
        self.assertEqual(atom.type, "TypE")

if __name__ == '__main__':
    unittest.main()
