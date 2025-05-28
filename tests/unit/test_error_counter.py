import unittest
from app import app, error_counter

class TestErrorCounter(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        error_counter.clear()  # Réinitialiser avant chaque test

    def test_error_counter_increments(self):
        self.client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'john@simplylift.co',
            'places': '15'
        })
        self.assertGreater(error_counter["club_ou_competition_introuvable"], 0)
