import unittest
from app import app

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_purchase_places_invalid_club_or_competition(self):
        response = self.client.post('/purchasePlaces', data={
            'club': 'Club Inexistant',
            'competition': 'Compétition Inexistante',
            'places': '2'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('Club ou competition introuvable.', response.get_data(as_text=True))
