from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        
    def test_game_board(self):
        with self.client:
            res = self.client.get('/')
            self.assertIn('game_board', session)
            self.assertIn(b'<p>High Score:', res.data)
            self.assertIn(b'Score:', res.data)
            self.assertIn(b'Time remaining:', res.data)
            
    def test_validate_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['game_board'] = [["K", "E", "V", "I", "N"], 
                                      ["K", "E", "V", "I", "N"], 
                                      ["K", "E", "V", "I", "N"], 
                                      ["K", "E", "V", "I", "N"], 
                                      ["K", "E", "V", "I", "N"]]
        res = self.client.get('/validate-word?word=kevin')
        self.assertEqual(res.json['result'], 'ok')
    
    def test_not_english_word(self):
        self.client.get('/')
        res = self.client.get('/validate-word?word=oiuwyeroiuqywe')
        self.assertEqual(res.json['result'], 'not-word')
        
    def test_non_valid_word(self):
        self.client.get('/')
        res = self.client.get('/validate-word?word=bus')
        self.assertEqual(res.json['result'], 'not-on-board')