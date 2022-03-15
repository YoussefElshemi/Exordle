from datetime import date
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
    last_used = models.DateField()
    num_correct_guesses = models.IntegerField(default=0)
    num_uses = models.IntegerField(default=0)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)

    def __str__(self):
        return self.word
    
    # get the last last-used word 
    def get_word():
        return Words.objects.all().order_by('last_used').first()
    
    def guess(self, request, attempt, save=True):
        
        # whether or not this is coming straight from a request or not
        if save:
            guess_num = attempt.pop('guess')
            attempt.pop('csrfmiddlewaretoken')
        
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
                data[position] = 'perfect'
                word = word.replace(value.upper(), ' ', 1)
            elif value.upper() in word:
                correct = False
                data[position] = 'correct'
                word = word.replace(value.upper(), ' ', 1)
            else:
                correct = False
                data[position] = 'wrong'
        
        # if we're saving the guess, insert into database
        if save:
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
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
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
