import unittest

from lib.json import Parser


class TestParsersJson(unittest.TestCase):
    def test_json_read(self):
        parser = Parser("data/bonds.json")

        self.assertTrue("bonds" in parser)
        self.assertTrue("length" in parser.bonds)
        self.assertTrue("test" in parser.bonds.length)
        self.assertEqual(["test", "100", "1.000"],
                         parser.bonds.length["test"].split())

    def test_json_section(self):
        bonds = Parser("data/bonds.json", "bonds")

        self.assertTrue("length" in bonds)
        self.assertTrue("test" in bonds.length)
        self.assertEqual(["test", "100", "1.000"],
                         bonds.length["test"].split())

    def test_include_file(self):
        elba = Parser("data/mol-elba.json")
        self.assertTrue("version" in elba)
        self.assertTrue("lipids" in elba.version)

        molecules = Parser("data/mol-elba.json", section="molecules")
        self.assertTrue("DOPC" in molecules)
        self.assertTrue("DOPE" in molecules)

    def test_missing_section(self):
        with self.assertRaises(KeyError):
            Parser("data/bonds.json", "potato")


if __name__ == '__main__':
    unittest.main()
