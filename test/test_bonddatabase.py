import unittest

from lib.bonddatabase import BondDatabase


class TestBondDatabase(unittest.TestCase):
    def test_open_database(self):
        db = BondDatabase()

    def test_read_database(self):
        db = BondDatabase()
        self.assertTrue("sugar-ring" in db.lengths)
        self.assertEqual(db.lengths["sugar-ring"].style, "harmonic")
        self.assertEqual(db.lengths["sugar-ring"].params, "200 1.520")

        self.assertTrue("sugar-ring" in db.angles)
        self.assertEqual(db.angles["sugar-ring"].style, "cosine/squared")
        self.assertEqual(db.angles["sugar-ring"].params, "120 110.0")

        self.assertTrue("sugar-dih-1" in db.dihedrals)
        self.assertEqual(db.dihedrals["sugar-dih-1"].style, "fourier")
        self.assertEqual(db.dihedrals["sugar-dih-1"].params, "2 1.00 3 0 0.25 1 -120")

        self.assertTrue("dipole-cone-1" in db.impropers)
        self.assertEqual(db.impropers["dipole-cone-1"].style, "dipole/cone")
        self.assertEqual(db.impropers["dipole-cone-1"].params, "200 120 60")

if __name__ == '__main__':
    unittest.main()
