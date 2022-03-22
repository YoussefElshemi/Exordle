from django.test import TestCase
    
class LeaderboardPageTests(TestCase):
    def test_leaderboard_page(self):
        response = self.client.get('/leaderboard/')
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'leaderboard/index.html')
