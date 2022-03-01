from django.contrib.auth.models import User
from django.db import models

class Locations(models.Model):
    location_id = models.IntegerField(primary_key=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    radius = models.IntegerField(default=50) 

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

class Words(models.Model):
    word = models.TextField(primary_key=True)
    last_used = models.DateField()
    num_correct_guesses = models.IntegerField(default=0)
    num_uses = models.IntegerField(default=0)
    location = models.OneToOneField(Locations, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.word

    class Meta:
        verbose_name = "Word"
        verbose_name_plural = "Words"

class Hints(models.Model):
    hint_id = models.IntegerField(primary_key=True)
    creator = models.OneToOneField(User, on_delete=models.CASCADE, related_name="creator")
    receiver = models.OneToOneField(User, on_delete=models.CASCADE, related_name="receiver")
    timestamp = models.DateTimeField()
    hint = models.TextField()

    def __str__(self) -> str:
        return self.hint


    class Meta:
        verbose_name = "Hint"
        verbose_name_plural = "Hints"

class Guesses(models.Model):
    guess_id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    guess = models.TextField(default="")
    guess_num = models.IntegerField(default=0)
    day_of_guess = models.DateField()
    correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.guess


    class Meta:
        verbose_name = "Guess"
        verbose_name_plural = "Guesses"
