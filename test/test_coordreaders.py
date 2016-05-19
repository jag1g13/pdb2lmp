import unittest

from lib.coordreaders import PDBReader, GROReader


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

    def test_parse_molecules(self):
        pdb = PDBReader("data/water.pdb")
        self.assertEqual(pdb.nmol, 31)
        self.assertEqual(pdb.molecules[0].name, "WAT")
        self.assertEqual(pdb.molecules[0].atoms, [0])

    def test_parse_cell(self):
        pdb = PDBReader("data/water.pdb")
        self.assertEqual(pdb.cell, [10, 10, 10, 90, 90, 90])


class TestGROReader(unittest.TestCase):
    def test_open_gro(self):
        gro = GROReader("data/water.gro")

    def test_parse_atoms(self):
        gro = GROReader("data/water.gro")
        self.assertEqual(gro.natoms, 31)
        self.assertEqual(gro.atoms[0].name, "O1")
        self.assertEqual(gro.atoms[0].resname, "WAT")
        self.assertAlmostEqual(gro.atoms[0].x, 1.84)
        self.assertAlmostEqual(gro.atoms[0].y, 6.96)
        self.assertAlmostEqual(gro.atoms[0].z, 2.34)

    def test_parse_molecules(self):
        gro = GROReader("data/water.gro")
        self.assertEqual(gro.nmol, 31)
        self.assertEqual(gro.molecules[0].name, "WAT")
        self.assertEqual(gro.molecules[0].atoms, [0])

    def test_parse_cell(self):
        gro = GROReader("data/water.gro")
        self.assertEqual(gro.cell, [10, 10, 10])


if __name__ == '__main__':
    unittest.main()
