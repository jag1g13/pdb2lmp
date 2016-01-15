import unittest

from pdb2lmp.atomdatabase import AtomDatabase


class TestAtomDatabase(unittest.TestCase):
    def test_open_database(self):
        db = AtomDatabase()

    def test_read_database_atoms(self):
        db = AtomDatabase()
        self.assertTrue("MEOH" in db.atoms)
        self.assertTrue("ETOH" in db.atoms)
        self.assertEqual(db.atoms["MEOH"].type, "MEOH")
        self.assertEqual(db.atoms["MEOH"].mass, 30.026)
        self.assertEqual(db.atoms["MEOH"].charge, 0)
        self.assertEqual(db.atoms["MEOH"].diameter, 12.7)
        self.assertEqual(db.atoms["MEOH"].rotmass, 30.026)
        self.assertEqual(db.atoms["ETOH"].mass, 44.053)

    def test_read_database_lj(self):
        db = AtomDatabase()
        self.assertTrue("MEOH" in db.lj_table_eps)
        self.assertTrue("ETOH" in db.lj_table_eps["MEOH"])
        self.assertEqual(db.lj_table_eps["MEOH"]["ETOH"], 1.25)

    def test_lj(self):
        db = AtomDatabase()
        self.helper_tuple_compare(db.lj("MEOH", "ETOH"), (3.963, 0.704))
        self.helper_tuple_compare(db.lj("WAT", "WAT"), (3.050, 0.550))
        self.helper_tuple_compare(db.lj("MEOH", "WAT"), (3.388, 0.621))
        self.helper_tuple_compare(db.lj("WAT", "MEOH"), (3.388, 0.621))

    def helper_tuple_compare(self, tup1, tup2):
        # Check each item in tuple to 3dp
        for item1, item2 in zip(tup1, tup2):
            self.assertAlmostEqual(item1, item2, 3)

if __name__ == '__main__':
    unittest.main()
