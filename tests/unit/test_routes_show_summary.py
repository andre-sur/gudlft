import unittest
from app import app

class TestShowSummary(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_show_summary_valid_email(self):
        response = self.client.post(
            '/showSummary',
            data={'email': 'admin@irontemple.com'},
            follow_redirects=True  # ← ici on suit la redirection 302
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Points", response.get_data(as_text=True))

    def test_show_summary_invalid_email(self):
        response = self.client.post(
            '/showSummary',
            data={'email': 'fake@email.com'},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Email inexistant.", response.get_data(as_text=True))
    

