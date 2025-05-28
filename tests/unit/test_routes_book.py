import unittest
from app import app

class TestBookRoute(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_book_valid(self):
        response = self.client.get('/book/Spring Festival/Simply Lift')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Booking for Spring Festival", response.get_data(as_text=True))

    def test_book_invalid_club(self):
        response = self.client.get('/book/Spring Festival/ClubInexistant')
        self.assertIn("Club ou competition introuvable", response.get_data(as_text=True))
