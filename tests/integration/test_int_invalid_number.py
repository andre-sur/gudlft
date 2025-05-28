import unittest
from app import app

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_purchase_places_invalid_number(self):
        response = self.client.post('/purchasePlaces', data={
            'club': 'Iron Temple',           # Un club valide
            'competition': 'Spring Festival', # Une compétition valide
            'places': 'abc'                  # Valeur non numérique
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("Nombre de places invalide.", response.get_data(as_text=True))
