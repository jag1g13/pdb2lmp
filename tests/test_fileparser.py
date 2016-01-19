import unittest

from lib.fileparser import FileParser


class TestFileParser(unittest.TestCase):
    watline = ['WAT', '18.015', '0', '3.050', '0.367', '0.541', '5.0']
    meoline = ['MEOH', '30.026', '0', '3.725', '0.536', '0.354', '12.7']

    def test_open_file(self):
        fp = FileParser("data/atoms.dat")

    def test_getline(self):
        fp = FileParser("data/atoms.dat")
        self.assertEqual(fp.getline(), self.watline)
        self.assertEqual(fp.section, "atomtypes")
        self.assertEqual(fp.getline(), self.meoline)

    def test_getline_number(self):
        fp = FileParser("data/mol.rtp")
        self.assertEqual(fp.nextsection(), "MEO")
        self.assertEqual(fp.nextsection(), "ETO")
        self.assertEqual(fp.nextsection(), "WAT")
        self.assertEqual(fp.getline(5), ["1", None, None, None, None])

    def test_findsection(self):
        fp = FileParser("data/atoms.dat")
        self.assertTrue(fp.findsection("atomtypes"))
        self.assertFalse(fp.findsection("potato"))

    def test_getlinefromsection(self):
        fp = FileParser("data/atoms.dat")
        self.assertEqual(fp.getlinefromsection("atomtypes"), self.watline)
        self.assertEqual(fp.getlinefromsection("atomtypes"), self.meoline)
        self.assertEqual(fp.getlinefromsection("nonbond_params"),
                         ['WAT', 'WAT', '1.5'])
        self.assertIsNone(fp.getlinefromsection("potato"))

    def test_nextsection(self):
        fp = FileParser("data/atoms.dat")
        self.assertEqual(fp.nextsection(), "atomtypes")
        self.assertEqual(fp.getline(), self.watline)
        self.assertEqual(fp.nextsection(), "nonbond_params")
        self.assertEqual(fp.getline(), ['WAT', 'WAT', '1.5'])
        self.assertIsNone(fp.nextsection())


if __name__ == '__main__':
    unittest.main()
