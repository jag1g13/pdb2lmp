import unittest

from ..pdb2lmp.atomdatabase import AtomDatabase


class TestAtomDatabase(unittest.TestCase):
    def test_open_database(self):
        db = AtomDatabase()

    def test_read_database(self):
        db = AtomDatabase()
        self.assertTrue("MEOH" in db.atoms)
        self.assertTrue("ETOH" in db.atoms)
        self.assertEqual(db.atoms["MEOH"].type, "MEOH")
        self.assertEqual(db.atoms["MEOH"].mass, 30.04)
        self.assertEqual(db.atoms["MEOH"].charge, -1)
        self.assertEqual(db.atoms["ETOH"].mass, 44.04)

if __name__ == '__main__':
    unittest.main()
