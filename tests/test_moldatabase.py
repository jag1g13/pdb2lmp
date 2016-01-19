import unittest

from lib.moldatabase import MolDatabase


class TestMolDatabase(unittest.TestCase):
    def test_open_database(self):
        db = MolDatabase()

    def test_read_database(self):
        db = MolDatabase()
        self.assertTrue("MEO" in db.molecules)
        self.assertTrue("ETO" in db.molecules)
        self.assertEqual(db.molecules["MEO"].atoms["C"].name, "C")
        self.assertEqual(db.molecules["MEO"].atoms["C"].type, "MEOH")

    def test_read_lengths(self):
        db = MolDatabase()
        self.assertEqual(db.molecules["GLC"].lengths[0].type, "sugar-ring")
        self.assertEqual(db.molecules["GLC"].lengths[0].atom1, "C1")
        self.assertEqual(db.molecules["GLC"].lengths[0].atom2, "C2")
        self.assertEqual(db.molecules["GLC"].lengths[5].type, "sugar-ring")
        self.assertEqual(db.molecules["GLC"].lengths[5].atom1, "O5")
        self.assertEqual(db.molecules["GLC"].lengths[5].atom2, "C1")

    def test_read_angles(self):
        db = MolDatabase()
        self.assertEqual(db.molecules["GLC"].angles[0].type, "sugar-ring")
        self.assertEqual(db.molecules["GLC"].angles[0].atom1, "C1")
        self.assertEqual(db.molecules["GLC"].angles[0].atom2, "C2")
        self.assertEqual(db.molecules["GLC"].angles[0].atom3, "C3")
        self.assertEqual(db.molecules["GLC"].angles[5].type, "sugar-ring")
        self.assertEqual(db.molecules["GLC"].angles[5].atom1, "O5")
        self.assertEqual(db.molecules["GLC"].angles[5].atom2, "C1")
        self.assertEqual(db.molecules["GLC"].angles[5].atom3, "C2")

if __name__ == '__main__':
    unittest.main()
