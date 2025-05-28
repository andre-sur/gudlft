import unittest
from app import app

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_purchase_places_insufficient_points(self):
        response = self.client.post('/purchasePlaces', data={
            'club': 'Iron Temple',           # Ce club a 4 points
            'competition': 'Spring Festival',
            'places': '9'                    # Demande plus que les points disponibles
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("Pas assez de points.", response.get_data(as_text=True))
