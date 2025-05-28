import unittest
from app import app

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_purchase_places_more_than_12(self):
        response = self.client.post('/purchasePlaces', data={
            'club': 'Iron Temple',          # Remplace par un nom réel de club
            'competition': 'Spring Festival',  # Remplace par une compétition existante
            'places': '13'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("Maximum 12 places.", response.get_data(as_text=True))
