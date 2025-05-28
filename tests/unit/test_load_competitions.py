import unittest
from app import loadCompetitions

class TestLoadCompetitions(unittest.TestCase):
    def test_load_competitions_returns_list(self):
        comps = loadCompetitions()
        self.assertIsInstance(comps, list)
        self.assertGreater(len(comps), 0)
        self.assertIn("name", comps[0])
