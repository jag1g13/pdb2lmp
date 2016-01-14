import unittest

from ..pdb2lmp.atomdatabase import AtomDatabase


class TestAtomDatabase(unittest.TestCase):
    def test_open_database(self):
        db = AtomDatabase()

    def test_read_database_atoms(self):
        db = AtomDatabase()
        self.assertTrue("MEOH" in db.atoms)
        self.assertTrue("ETOH" in db.atoms)
        self.assertEqual(db.atoms["MEOH"].type, "MEOH")
        self.assertEqual(db.atoms["MEOH"].mass, 30.04)
        self.assertEqual(db.atoms["MEOH"].charge, -1)
        self.assertEqual(db.atoms["ETOH"].mass, 44.04)

    def test_read_database_lj(self):
        db = AtomDatabase()
        self.assertTrue("MEOH" in db.lj_table_eps)
        self.assertTrue("ETOH" in db.lj_table_eps["MEOH"])
        self.assertEqual(db.lj_table_eps["MEOH"]["ETOH"], -1)

    def test_lj(self):
        db = AtomDatabase()
        self.assertEqual(db.lj("MEOH", "ETOH"), (-1, -1))
        self.assertEqual(db.lj("WAT", "WAT"), (-1, 1))
        self.assertEqual(db.lj("MEOH", "WAT"), (-1, 0))
        self.assertEqual(db.lj("WAT", "MEOH"), (-1, 0))

if __name__ == '__main__':
    unittest.main()
