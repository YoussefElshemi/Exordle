from django.utils import timezone
from django.test import TestCase

from auth.models import GameUser
from .models import Guesses, Words, Locations, Hints
from django.contrib.auth.models import User

class WordTestCase(TestCase):
    def setUp(self):
        location = Locations.objects.create(latitude=0, longitude=0, radius=0)
        Words.objects.create(word="FORUM", 
                             date=timezone.now(), 
                             num_correct_guesses=0, 
                             num_uses=0, 
                             location=location)
        
    def test_word_location(self):
        """Ensures that a location is associated with a word"""
        word = Words.objects.get(word="FORUM")
        location = Locations.objects.all()[0]
        
        self.assertEqual(word.location, location)
        
    def test_word__str__(self):
        """Ensures __str__ works for word"""
        word = Words.objects.get(word="FORUM")
        
        self.assertEqual(str(word), "FORUM")

        
    def test_all_correct_word(self):
        """Testing a complete correct word"""
        word = Words.objects.get(word="FORUM")
        
        attempt = { "1": "F", "2": "O", "3": "R", "4": "U", "5": "M" }
        response = word.guess({}, attempt, False)
        correct_response = { "1": "perfect", "2": "perfect", "3": "perfect", "4": "perfect", "5": "perfect" }
        self.assertEqual(response, correct_response)

    def test_partially_correct_word(self):
        """Testing a partially correct word"""
        word = Words.objects.get(word="FORUM")
        
        attempt = { "1": "F", "2": "X", "3": "R", "4": "X", "5": "M" }
        response = word.guess({}, attempt, False)
        correct_response = { "1": "perfect", "2": "wrong", "3": "perfect", "4": "wrong", "5": "perfect" }
        self.assertEqual(response, correct_response)
        
    def test_all_wrong_word(self):
        """Testing a complete wrong word"""
        word = Words.objects.get(word="FORUM")
        
        attempt = { "1": "X", "2": "X", "3": "X", "4": "X", "5": "X" }
        response = word.guess({}, attempt, False)
        correct_response = { "1": "wrong", "2": "wrong", "3": "wrong", "4": "wrong", "5": "wrong" }
        self.assertEqual(response, correct_response)
        
        
class TestPOSTRequests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", password="12345")
        other_user = User.objects.create_user(username="testuser2", password="12345")
        GameUser.objects.create(user=user, points=0, wins=0)
        location = Locations.objects.create(latitude=0, longitude=0, radius=0)
        word = Words.objects.create(word="FORUM", 
                             date=timezone.now(), 
                             num_correct_guesses=0, 
                             num_uses=0, 
                             location=location)
        
        Hints.objects.create(hint_code="000000", 
                             creator=other_user, 
                             receiver=None, 
                             word=word, 
                             timestamp=timezone.now(), 
                             hint="FO")

        
    def test_submit_guess(self):
        """Testing guess endpoint"""
        self.client.login(username="testuser", password="12345")
        data = { "guess": 1, "csrfmiddlewaretoken": "", "1": "F", "2": "O", "3": "R", "4": "U", "5": "M" }
        
        response = self.client.post("/check/", data)
        correct_response = { "1": "perfect", "2": "perfect", "3": "perfect", "4": "perfect", "5": "perfect", "valid": True, "success": True }
        
        self.assertEqual(response.json(), correct_response)
        self.assertEqual(Guesses.objects.count(), 1)
        

    def test_create_hint(self):
        """Testing the creation of hints"""
        self.client.login(username="testuser", password="12345")
        data = { "csrfmiddlewaretoken": "" }
        
        response = self.client.post("/qr/", data)
        self.assertIsNotNone(response.json()["code"])
        self.assertIsNotNone(response.json()["svg"])
        self.assertEqual(Hints.objects.count(), 2)

    def test_use_hint(self):
        """Testing using hints"""
        self.client.login(username="testuser", password="12345")
        data = { "csrfmiddlewaretoken": "", "code": "000000" }
        
        response = self.client.post("/hint/", data)
        correct_response = [{'letter': 'F', 'result': 'correct'}, {'letter': 'O', 'result': 'correct'}]

        self.assertEqual(response.json()["success"], True)
        self.assertEqual(response.json()["data"], correct_response)
        
    def test_login_redirect(self):
        """Test if you are redirected to login when you try to play"""
        response = self.client.get("/play/")
        
        self.assertEqual(response.url, "/auth/login")
    
    def test_map_search(self):
        """Test if the co-ordinates are returned from a search"""
        self.client.login(username="testuser", password="12345")
        data = { "csrfmiddlewaretoken": "", "search": "FORUM" }
        
        response = self.client.post("/map/search/", data)
        self.assertEqual(response.json()["success"], True)
        self.assertEqual(response.json()["lng"], 0)
        self.assertEqual(response.json()["lat"], 0)
