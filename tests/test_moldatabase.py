import unittest

from ..pdb2lmp.moldatabase import MolDatabase


class TestMolDatabase(unittest.TestCase):
    def test_open_database(self):
        db = MolDatabase("mol.rtp")

    def test_read_database(self):
        db = MolDatabase("mol.rtp")
        self.assertTrue("MEOH" in db.molecules)
        self.assertTrue("ETOH" in db.molecules)
        self.assertTrue("C" in db.molecules["MEOH"].atoms)
        self.assertEqual(db.molecules["MEOH"].atoms["C"].name, "C")
        self.assertEqual(db.molecules["MEOH"].atoms["C"].type, "MEOH")
        self.assertEqual(db.molecules["MEOH"].atoms["C"].charge, 0)

if __name__ == '__main__':
    unittest.main()
