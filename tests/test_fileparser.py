import unittest

from ..pdb2lmp.fileparser import FileParser


class TestFileParser(unittest.TestCase):
    def test_open_file(self):
        fp = FileParser("data/atoms.dat")

    def test_getline(self):
        fp = FileParser("data/atoms.dat")
        self.assertEqual(fp.getline(), ['WAT', '18.015', '0', '3.050', '0.367'])
        self.assertEqual(fp.section, "atomtypes")
        self.assertEqual(fp.getline(), ['MEOH', '30.026', '0', '3.725', '0.536'])

    def test_getline_number(self):
        fp = FileParser("data/mol.rtp")
        self.assertEqual(fp.nextsection(), "MEOH")
        self.assertEqual(fp.nextsection(), "ETOH")
        self.assertEqual(fp.nextsection(), "WAT")
        self.assertEqual(fp.getline(5), ["1", None, None, None, None])

    def test_findsection(self):
        fp = FileParser("data/atoms.dat")
        self.assertTrue(fp.findsection("atomtypes"))
        self.assertFalse(fp.findsection("potato"))

    def test_getlinefromsection(self):
        fp = FileParser("data/atoms.dat")
        self.assertEqual(fp.getlinefromsection("atomtypes"),
                         ['WAT', '18.015', '0', '3.050', '0.367'])
        self.assertEqual(fp.getlinefromsection("atomtypes"),
                         ['MEOH', '30.026', '0', '3.725', '0.536'])
        self.assertEqual(fp.getlinefromsection("nonbond_params"),
                         ['WAT', 'WAT', '1.5'])
        self.assertIsNone(fp.getlinefromsection("potato"))

    def test_nextsection(self):
        fp = FileParser("data/atoms.dat")
        self.assertEqual(fp.nextsection(), "atomtypes")
        self.assertEqual(fp.getline(), ['WAT', '18.015', '0', '3.050', '0.367'])
        self.assertEqual(fp.nextsection(), "nonbond_params")
        self.assertEqual(fp.getline(), ['WAT', 'WAT', '1.5'])
        self.assertIsNone(fp.nextsection())


if __name__ == '__main__':
    unittest.main()
