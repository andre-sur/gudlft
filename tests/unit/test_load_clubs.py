import unittest
from app import loadClubs

class TestLoadClubs(unittest.TestCase):
    def test_load_clubs_returns_list(self):
        clubs = loadClubs()
        self.assertIsInstance(clubs, list)
        self.assertGreater(len(clubs), 0)
        self.assertIn("name", clubs[0])
