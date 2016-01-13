import unittest

from ..pdb2lmp.pdbreader import PDBReader

class TestPDBReader(unittest.TestCase):
    def test_open_pdb(self):
        pdb = PDBReader("data/water.pdb")

    def test_parse_atoms(self):
        pdb = PDBReader("data/water.pdb")
        self.assertEqual(pdb.natoms, 31)
        self.assertEqual(pdb.atoms[0].name, "O1")
        self.assertEqual(pdb.atoms[0].resname, "WAT")
        self.assertEqual(pdb.atoms[0].x, 1.837)
        self.assertEqual(pdb.atoms[0].y, 6.961)
        self.assertEqual(pdb.atoms[0].z, 2.338)


if __name__ == '__main__':
    unittest.main()
