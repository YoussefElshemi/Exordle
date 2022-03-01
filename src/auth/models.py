from django.contrib.auth.models import User
from django.db import models


class GameUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
