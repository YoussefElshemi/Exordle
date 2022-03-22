from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User

from game.models import Locations, Words

class TestPOSTRequests(TestCase):
    def setUp(self):
        User.objects.create_user(username="testuser", password="12345")
        location = Locations.objects.create(latitude=0, longitude=0, radius=0)
        Words.objects.create(word="FORUM", 
                             date=timezone.now(), 
                             num_correct_guesses=0, 
                             num_uses=0, 
                             location=location)
        
    def test_search(self):
        self.client.login(username="testuser", password="12345")
        data = { "crsfmiddlewaretoken": "", "search": "FORUM" }
        response = self.client.post('/map/search/', data)

        self.assertEquals(response.json()["success"], True)
        self.assertEquals(response.json()["lng"], 0)
        self.assertEquals(response.json()["lat"], 0)


class MapPageTests(TestCase):
    def test_map_page(self):
        response = self.client.get('/map/')
                
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'map/index.html')
