import unittest

from pdb2lmp import PDB2LMP


class TestPDB2LMP(unittest.TestCase):
    def test_read_data(self):
        conv = PDB2LMP("data/water.pdb")

    def test_collect_types(self):
        conv = PDB2LMP("data/water.pdb")
        conv.collect_types()
        self.assertEquals(conv.moltypes, ["WAT"])
        self.assertEquals(conv.atomtypes, ["WAT"])

    def test_collect_types_full(self):
        conv = PDB2LMP("data/glc.pdb")
        conv.collect_types()
        self.assertEqual(conv.moltypes, ["GLC"])
        self.assertEqual(conv.atomtypes, ["MEOH", "ETOH", "OXY"])
        self.assertEqual(conv.lentypes, ["sugar-ring"])
        self.assertEqual(conv.angtypes, ["sugar-ring"])
        self.assertEqual(conv.natoms.total, 6)
        self.assertEqual(conv.natoms.types, 3)
        self.assertEqual(conv.nlengths.total, 6)
        self.assertEqual(conv.nlengths.types, 1)
        self.assertEqual(conv.nangles.total, 6)
        self.assertEqual(conv.nangles.types, 1)

    def test_populate_pdb_data(self):
        conv = PDB2LMP("data/water.pdb")
        conv.collect_types()
        conv.populate_pdb_data()
        self.assertEqual(conv.pdb.atoms[0].type, "WAT")

    def test_write_data(self):
        conv = PDB2LMP("data/water.pdb")
        conv.collect_types()
        conv.populate_pdb_data()
        conv.write_data("test.data")

    def test_write_forcefield(self):
        conv = PDB2LMP("data/water.pdb")
        conv.collect_types()
        conv.populate_pdb_data()
        conv.write_forcefield("test.ff")

    def test_write_forcefield_mixed(self):
        conv = PDB2LMP("data/mixed.pdb")
        conv.collect_types()
        conv.populate_pdb_data()
        conv.write_forcefield("mixed.ff")

    def test_glc(self):
        conv = PDB2LMP("data/glc.pdb")
        conv.collect_types()
        conv.populate_pdb_data()
        conv.write_data("glc.data")
        conv.write_forcefield("glc.ff")

if __name__ == '__main__':
    unittest.main()