import unittest

from ..pdb2lmp.fileparser import FileParser


class TestFileParser(unittest.TestCase):
    def test_open_file(self):
        fp = FileParser("data/atoms.dat")

    def test_getline(self):
        fp = FileParser("data/atoms.dat")
        self.assertEqual(fp.getline(), ['MEOH', '30.04', '-1', '-1', '-1'])
        self.assertEqual(fp.section, "atomtypes")
        self.assertEqual(fp.getline(), ['ETOH', '44.04', '-1', '-1', '-1'])
        self.assertEqual(fp.getline(), ['MEOH', 'MEOH', '-1', '-1'])
        self.assertEqual(fp.section, "nonbond_params")

    def test_findsection(self):
        fp = FileParser("data/atoms.dat")
        self.assertTrue(fp.findsection("atomtypes"))
        self.assertFalse(fp.findsection("potato"))

    def test_getlinefromsection(self):
        fp = FileParser("data/atoms.dat")
        self.assertEqual(fp.getlinefromsection("atomtypes"),
                         ['MEOH', '30.04', '-1', '-1', '-1'])
        self.assertEqual(fp.getlinefromsection("atomtypes"),
                         ['ETOH', '44.04', '-1', '-1', '-1'])
        self.assertIsNone(fp.getlinefromsection("atomtypes"))
        self.assertEqual(fp.getlinefromsection("nonbond_params"),
                         ['MEOH', 'MEOH', '-1', '-1'])
        self.assertIsNone(fp.getlinefromsection("potato"))

    def test_nextsection(self):
        fp = FileParser("data/atoms.dat")
        self.assertEqual(fp.nextsection(), "atomtypes")
        self.assertEqual(fp.getline(), ['MEOH', '30.04', '-1', '-1', '-1'])
        self.assertEqual(fp.nextsection(), "nonbond_params")
        self.assertEqual(fp.getline(), ['MEOH', 'MEOH', '-1', '-1'])
        self.assertIsNone(fp.nextsection())


if __name__ == '__main__':
    unittest.main()
