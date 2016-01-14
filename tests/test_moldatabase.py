import unittest

from ..pdb2lmp.moldatabase import MolDatabase


class TestMolDatabase(unittest.TestCase):
    def test_open_database(self):
        db = MolDatabase()

    def test_read_database(self):
        db = MolDatabase()
        self.assertTrue("MEOH" in db.molecules)
        self.assertTrue("ETOH" in db.molecules)
        self.assertEqual(db.molecules["MEOH"].atoms[0].name, "C")
        self.assertEqual(db.molecules["MEOH"].atoms[0].type, "MEOH")

if __name__ == '__main__':
    unittest.main()
