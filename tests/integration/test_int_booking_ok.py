import unittest
from app import app

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_purchase_places_success(self):
        response = self.client.post('/purchasePlaces', data={
            'club': 'Iron Temple',               # Nom exact du club dans clubs.json
            'competition': 'Fall Classic', # Nom exact de la compétition
            'places': '4'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Réservation confirmée.', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
