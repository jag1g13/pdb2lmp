import unittest

from lib.bonddatabase import BondDatabase

class TestBondDatabase(unittest.TestCase):
    def test_open_database(self):
        db = BondDatabase()

    def test_read_database(self):
        db = BondDatabase()
        self.assertTrue("sugar-ring" in db.lengths)
        self.assertEqual(db.lengths["sugar-ring"].style, "harmonic")
        self.assertEqual(db.lengths["sugar-ring"].k, 200)
        self.assertEqual(db.lengths["sugar-ring"].r, 1.520)

if __name__ == '__main__':
    unittest.main()
