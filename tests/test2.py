from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

    def tearDown(self):
        """Stuff to do after each test."""

    def test_homepage(self):

        """Test to confirm information is in the session and HTML is displayed"""
        with app.test_client() as client:
                resp = client.get('/')
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn('<h2>Boggle Game</h2>', html)
                self.assertEqual(session.get('highscore'), None)
                self.assertEqual(session.get('nplays'), None)


    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        resp = client.get('/check-word?word=cat')
        self.assertEqual(resp.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""
        with app.test_client() as client:

            client.get('/')  
            resp = client.get('/check-word?word=impossible')
            self.assertEqual(resp.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if word is on the board"""
        with app.test_client() as client:

            client.get('/')
            resp = client.get('/check-word?word=fsjdakfkldsfjdslkfjdlksf')
            self.assertEqual(resp.json['result'], 'not-word')

    