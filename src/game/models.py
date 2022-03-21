from datetime import date, timezone
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# location model
class Locations(models.Model):
    location_id = models.AutoField(primary_key=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    radius = models.IntegerField(default=50) 

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

# word model
class Words(models.Model):
    word = models.TextField(primary_key=True, max_length=20)
    date = models.DateField()
    num_correct_guesses = models.IntegerField(default=0)
    num_uses = models.IntegerField(default=0)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)

    def __str__(self):
        return self.word
    
    # get the last last-used word 
    def get_word():
        try:
            return Words.objects.get(date=timezone.now()) # get word of the day
        except:
            try:
                return Words.objects.all()[0] # get first word
            except:
                return "BLANK" # if no words, return word as BLANK

    def get_valid_words(self):
        word_file = open(os.path.join(settings.BASE_DIR, '..', 'res', 'words.txt'), "r")
        word_file = [x.strip() for x in word_file.readlines()]
        db_words = list(map(str.lower, map(str, Words.objects.all())))

        return db_words + word_file
    
    def guess_letter(self, letter):
        word = str(self)
        
        if letter in word:
            return "correct"
        else:
            return "wrong"

    
    def guess(self, request, attempt, save=True):
        
        # whether or not this is coming straight from a request or not
        if save:
            guess_num = attempt.pop("guess")
            attempt.pop("csrfmiddlewaretoken")
        
        correct = True
        word = str(self)
        guess_attempt = ""
        data = {}
        
        # assign letters their respective value based on correctness
        # perfect = green
        # correct = yellow
        # wrong = grey
        
        for position, value in attempt.items():
            guess_attempt += value
            idx = int(position) - 1
            if word[idx] == value.upper():
                data[position] = "perfect"
                word = word.replace(value.upper(), " ", 1)
            elif value.upper() in word:
                correct = False
                data[position] = "correct"
                word = word.replace(value.upper(), " ", 1)
            else:
                correct = False
                data[position] = "wrong"
        
        # if we're saving the guess, insert into database
        if save:
            data["valid"] = guess_attempt.lower() in self.get_valid_words()
            
            if data["valid"]:
                guess_item = Guesses.objects.create(
                    user=request.user, 
                    word=self,
                    guess=guess_attempt.upper(), 
                    guess_num=guess_num, 
                    day_of_guess=date.today(),
                    correct=correct
                )
                
                guess_item.save()
                
        return data

    class Meta:
        verbose_name = "Word"
        verbose_name_plural = "Words"

# hint model
class Hints(models.Model):
    hint_id = models.AutoField(primary_key=True)
    hint_code = models.TextField(default=None)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver", null=True, blank=True)
    word = models.ForeignKey(Words, on_delete=models.CASCADE, default=None)
    timestamp = models.DateTimeField()
    hint = models.TextField()

    def __str__(self):
        return self.hint

    class Meta:
        verbose_name = "Hint"
        verbose_name_plural = "Hints"
        
# guess model
class Guesses(models.Model):
    guess_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Words, on_delete=models.CASCADE, default=None)
    guess = models.TextField(default="")
    guess_num = models.IntegerField(default=0)
    day_of_guess = models.DateField()
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.guess

    class Meta:
        verbose_name = "Guess"
        verbose_name_plural = "Guesses"

class CheckIns(models.Model):
    checkin_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Words, on_delete=models.CASCADE, default=None)
    points = models.IntegerField(default=0)
    day = models.DateField()
    
    class Meta:
        verbose_name = "Check In"
        verbose_name_plural = "Check Ins"