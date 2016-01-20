import unittest

from lib.bonddatabase import BondDatabase

class TestBondDatabase(unittest.TestCase):
    def test_open_database(self):
        db = BondDatabase()

    def test_read_database(self):
        db = BondDatabase()
        self.assertTrue("sugar-ring" in db.lengths)
        self.assertEqual(db.lengths["sugar-ring"], "harmonic 200 1.520")
        self.assertTrue("sugar-ring" in db.angles)
        self.assertEqual(db.angles["sugar-ring"], "cosine/squared 120 110.0")

if __name__ == '__main__':
    unittest.main()
