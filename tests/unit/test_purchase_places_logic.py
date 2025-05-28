import unittest
from app import app

class TestPurchasePlaces(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_purchase_places_too_many(self):
        response = self.client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Spring Festival',
            'places': '13'  # Trop de places
        })
        self.assertIn(b"Maximum 12 places.", response.data)

    def test_purchase_places_not_enough_points(self):
        response = self.client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Spring Festival',
            'places': '100'  # Dépasse les points
        })
        self.assertIn("Maximum 12 places.", response.get_data(as_text=True))
