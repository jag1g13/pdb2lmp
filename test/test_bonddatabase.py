import unittest

from lib.bonddatabase import BondDatabase


class TestBondDatabase(unittest.TestCase):
    def test_open_database(self):
        db = BondDatabase()

    def test_read_database(self):
        db = BondDatabase()
        self.assertTrue("sugar-ring" in db.length)
        self.assertEqual(db.length["sugar-ring"].style, "harmonic")
        self.assertEqual(db.length["sugar-ring"].params, "200 1.520")

        self.assertTrue("sugar-ring" in db.angle)
        self.assertEqual(db.angle["sugar-ring"].style, "cosine/squared")
        self.assertEqual(db.angle["sugar-ring"].params, "120 110.0")

        self.assertTrue("sugar-dih-1" in db.dihedral)
        self.assertEqual(db.dihedral["sugar-dih-1"].style, "fourier")
        self.assertEqual(db.dihedral["sugar-dih-1"].params, "2 1.00 3 0 0.25 1 -120")

if __name__ == '__main__':
    unittest.main()
