import unittest

from ..pdb2lmp.pdb2lmp import PDB2LMP


class TestPDB2LMP(unittest.TestCase):
    def test_read_data(self):
        conv = PDB2LMP("data/water.pdb")

    def test_collect_types(self):
        conv = PDB2LMP("data/water.pdb")
        conv.collect_types()
        self.assertEquals(conv.moltypes, ["WAT"])
        self.assertEquals(conv.atomtypes, ["WAT"])

    def test_write_data(self):
        conv = PDB2LMP("data/water.pdb")
        conv.collect_types()
        conv.write_data("data.wat")

if __name__ == '__main__':
    unittest.main()
