import unittest
from app import app

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_purchase_places_insufficient_competition_slots(self):
        response = self.client.post('/purchasePlaces', data={
            'club': 'Iron Temple',
            'competition': 'Fall Classic',   # Cette competition a 13 places
            'places': '20'                   # Demande plus que le disponible
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("Maximum 12 places.", response.get_data(as_text=True))
