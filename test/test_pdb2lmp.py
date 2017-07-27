import unittest

from pdb2lmp import PDB2LMP


class TestPDB2LMP(unittest.TestCase):
    def test_read_data(self):
        conv = PDB2LMP("test/data/water.pdb")

    def test_collect_types(self):
        conv = PDB2LMP("test/data/water.pdb")
        conv.collect_types()
        self.assertListEqual(conv.moltypes, ["WAT"])
        self.assertListEqual(conv.atomtypes, ["WAT"])

    def test_collect_types_full(self):
        conv = PDB2LMP("test/data/glc.pdb")
        conv.collect_types()
        self.assertListEqual(conv.moltypes, ["0GA"])
        self.assertListEqual(conv.atomtypes, ["MEOH", "ETOH", "OXY", "WAT"])
        self.assertListEqual(conv.lentypes, ["sugar-ring"])
        self.assertListEqual(conv.angtypes, ["sugar-ring"])
        self.assertEqual(conv.natoms.total, 6)
        self.assertEqual(conv.natoms.types, 4)
        self.assertEqual(conv.nlengths.total, 6)
        self.assertEqual(conv.nlengths.types, 1)
        self.assertEqual(conv.nangles.total, 6)
        self.assertEqual(conv.nangles.types, 1)
        self.assertEqual(conv.ndihedrals.total, 6)
        self.assertEqual(conv.ndihedrals.types, 2)
        self.assertEqual(conv.nimpropers.total, 5)
        self.assertEqual(conv.nimpropers.types, 2)

    def test_collect_types_no_add_water(self):
        conv = PDB2LMP("test/data/glc.pdb")
        conv.collect_types(add_water=False)
        self.assertListEqual(conv.moltypes, ["0GA"])
        self.assertListEqual(conv.atomtypes, ["MEOH", "ETOH", "OXY"])
        self.assertEqual(conv.natoms.total, 6)
        self.assertEqual(conv.natoms.types, 3)

    def test_collect_types_subset(self):
        conv = PDB2LMP("test/data/ala-aa.gro")
        conv.collect_types(allow_atom_subset=True)
        self.assertListEqual(conv.moltypes, ["0NA"])
        self.assertListEqual(conv.atomtypes, ["MEOH", "ETOH", "OXY", "WAT"])
        self.assertEqual(conv.natoms.total, 6)
        self.assertEqual(conv.natoms.types, 4)

    def test_collect_types_multiple_residues(self):
        conv = PDB2LMP("test/data/glc_crystal.gro")
        conv.collect_types()
        self.assertListEqual(conv.moltypes, ["0GB"])
        self.assertListEqual(conv.atomtypes, ["MEOH", "ETOH", "OXY", "WAT"])
        self.assertListEqual(conv.lentypes, ["sugar-ring"])
        self.assertListEqual(conv.lentypes, ["sugar-ring"])
        self.assertListEqual(conv.angtypes, ["sugar-ring"])
        self.assertEqual(conv.natoms.total, 576)
        self.assertEqual(conv.natoms.types, 4)
        self.assertEqual(conv.nlengths.total, 576)
        self.assertEqual(conv.nlengths.types, 1)
        self.assertEqual(conv.nangles.total, 576)
        self.assertEqual(conv.nangles.types, 1)
        self.assertEqual(conv.ndihedrals.total, 576)
        self.assertEqual(conv.ndihedrals.types, 2)
        self.assertEqual(conv.nimpropers.total, 480)
        self.assertEqual(conv.nimpropers.types, 2)

    def test_populate_pdb_data(self):
        conv = PDB2LMP("test/data/water.pdb")
        conv.collect_types()
        conv.populate_pdb_data()
        self.assertEqual(conv.coords.atoms[0].type, "WAT")

    def test_write_data(self):
        conv = PDB2LMP("test/data/water.pdb")
        conv.collect_types()
        conv.populate_pdb_data()
        conv.write_data("water.data")

    def test_write_forcefield(self):
        conv = PDB2LMP("test/data/water.pdb")
        conv.collect_types()
        conv.populate_pdb_data()
        conv.write_forcefield("water.ff")

    def test_write_forcefield_mixed(self):
        conv = PDB2LMP("test/data/mixed.pdb")
        conv.collect_types()
        conv.populate_pdb_data()
        conv.write_forcefield("mixed.ff")

    def test_glc(self):
        conv = PDB2LMP("test/data/glc.pdb")
        conv.collect_types()
        conv.populate_pdb_data()
        conv.write_data("glc.data")
        conv.write_forcefield("glc.ff")

    def test_gro(self):
        conv = PDB2LMP("test/data/water.gro")
        conv.collect_types()
        conv.populate_pdb_data()
        conv.write_data("from_gro.data")
        conv.write_forcefield("from_gro.ff")

if __name__ == '__main__':
    unittest.main()
