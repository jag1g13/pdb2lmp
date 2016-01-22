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
        self.assertEqual(db.molecules["GLC"].lengths[0].atoms[0], "C1")
        self.assertEqual(db.molecules["GLC"].lengths[0].atoms[1], "C2")
        self.assertEqual(db.molecules["GLC"].lengths[5].type, "sugar-ring")
        self.assertEqual(db.molecules["GLC"].lengths[5].atoms[0], "O5")
        self.assertEqual(db.molecules["GLC"].lengths[5].atoms[1], "C1")

    def test_read_angles(self):
        db = MolDatabase()
        self.assertEqual(db.molecules["GLC"].angles[0].type, "sugar-ring")
        self.assertEqual(db.molecules["GLC"].angles[0].atoms[0], "C1")
        self.assertEqual(db.molecules["GLC"].angles[0].atoms[1], "C2")
        self.assertEqual(db.molecules["GLC"].angles[0].atoms[2], "C3")
        self.assertEqual(db.molecules["GLC"].angles[5].type, "sugar-ring")
        self.assertEqual(db.molecules["GLC"].angles[5].atoms[0], "O5")
        self.assertEqual(db.molecules["GLC"].angles[5].atoms[1], "C1")
        self.assertEqual(db.molecules["GLC"].angles[5].atoms[2], "C2")

if __name__ == '__main__':
    unittest.main()
