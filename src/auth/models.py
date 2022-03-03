from django.contrib.auth.models import User
from django.db import models

# extending user model to also include points and wins
class GameUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
