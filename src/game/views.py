from cmath import exp
from datetime import datetime, timedelta
import random
import string
import math
from io import BytesIO
import qrcode
import qrcode.image.svg
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.utils import timezone

from auth.models import GameUser
from .models import Guesses, Hints, Words, CheckIns

def index(request):
    context = {
        'user': request.user
    }

    # push user object to front-end
    return render(request, 'game/index.html', context)

def play(request):
    # only accessible if user is logged in
    if request.user.is_authenticated:
        
        # create game_user object
        try: 
            game_user = GameUser.objects.get(user=request.user)
        except:
            game_user = GameUser.objects.create(user=request.user, points=0, wins=0)
                    
        # get word of the day and previous guesses for this word if there are any
        word = Words.get_word()
        guesses = Guesses.objects.filter(user=request.user, word=word, day_of_guess=datetime.now()) 
        hints = Hints.objects.filter(receiver=request.user, word=word, 
                                     timestamp__gte=timezone.now().replace(hour=0, minute=0, second=0), 
                                     timestamp__lte=timezone.now().replace(hour=23, minute=59, second=59))
        
                    
        try:
            CheckIns.objects.get(user=request.user, word=word, day=datetime.now())
            checked_in = True
        except:
            checked_in = False
            
        css_guesses = []
        css_keyboard = []
        success = False
        
        for guess in guesses:
            if guess.correct:
                success = True
                
                
            guess_object = make_guess(str(guess))
            response = word.guess(request, guess_object, False)
            css_guesses.append(list(response.values()))
            
            for idx, result in response.items():
                css_keyboard.append({ "letter": str(guess)[idx - 1], "result": result })   
        
        for hint in hints:
            for letter in str(hint):
                css_keyboard.append({ "letter": letter, "result": word.guess_letter(letter) })

          
        length = len(str(word)) + 1
        
        context = {
            'game_user': game_user,
            'user': request.user,
            'guesses': guesses,
            'success': success,
            'checked_in': checked_in,
            'css_guesses': css_guesses,
            'css_keyboard': css_keyboard,
            'word_range': range(1, length),
            'guess_range': range(1, length + 1)
        }

        return render(request, 'game/play.html', context)

    # redirect to login if they aren't logged in
    return redirect('/auth/login')

def check(request):
    # ensure user is logged in
    if request.method == 'POST' and request.user.is_authenticated:
        
        # get the guess data and return it as JSON
        word = Words.get_word()
        data = word.guess(request, request.POST.dict())    
        
        success = True
        for value in data.values():
            if value == "wrong" or value == "correct":
                success = False
        
        if success:            
            word.num_correct_guesses += 1
            word.save()

        data["success"] = success
        return JsonResponse(data)

    return None

def qr_code(request):
    # ensure user is logged in
    if request.method == 'POST' and request.user.is_authenticated:
            
        # generate a random 6 digit code
        code = str(random.randint(0, 999999))
        padded_code = code.zfill(6)
        hint_length = 3 if request.user.groups.filter(name='Lecturer').exists() else 2
        
        hint = ''.join(random.sample(string.ascii_uppercase, hint_length))
        
        hint_object = Hints.objects.create(
            hint_code=padded_code,
            creator=request.user,
            word=Words.get_word(),
            timestamp=timezone.now(),
            hint=hint
        )
        
        hint_object.save()

        # generate and return SVG for QR code representing the 6 digit code
        factory = qrcode.image.svg.SvgPathImage
        img = qrcode.make(padded_code, image_factory=factory, box_size=20)
        stream = BytesIO()
        img.save(stream)

        return JsonResponse({ 'svg': stream.getvalue().decode(), 'code': padded_code })

    return None

def check_in(request):
    # ensure user is logged in
    if request.method == 'POST' and request.user.is_authenticated:
        word = Words.get_word()
        
        try:
            CheckIns.objects.get(user=request.user, word=word, day=datetime.now())
            checked_in = True
        except:
            checked_in = False
            
        if checked_in:
            return JsonResponse({ "success": False, "message": "You are already checked in" })
        
        user_location = {
            "latitude": float(request.POST.get("latitude")),
            "longitude": float(request.POST.get("longitude"))
        }
               
        # calcuate distance between user's current location and the word's location                                 
        distance = get_distance(word.location, user_location)
        
        # if they are within the the radius                
        if (distance < word.location.radius):
            guesses = Guesses.objects.filter(user=request.user, word=word, day_of_guess=datetime.now()) 
            hints = Hints.objects.filter(receiver=request.user, word=word, 
                                     timestamp__gte=timezone.now().replace(hour=0, minute=0, second=0), 
                                     timestamp__lte=timezone.now().replace(hour=23, minute=59, second=59))
            
            points = len(str(word)) * 100 + 300
            points -= guesses.count() * 100
            points -= hints.count() * 100
            
            game_user = GameUser.objects.get(user=request.user)
            game_user.points += points
            game_user.wins += 1
            game_user.save()
            
            CheckIns.objects.create(user=request.user, word=word, points=points, day=datetime.now())
            
            return JsonResponse({ "success": True, "points": points }) 
        else:
            message = f"Successfully checked in, received {points} points"
            return JsonResponse({ "success": False, "message": message })
        
    return None

def hint(request):
    # ensure user is logged in
    if request.method == 'POST' and request.user.is_authenticated:
        code = request.POST.get("code")
        
        try:
            # get hint used within last 5 minutes
            used_hint = Hints.objects.get(receiver=request.user, timestamp__gte=(timezone.now() - timedelta(minutes=5)))
            
            time = timedelta(minutes=5) - (timezone.now() - used_hint.timestamp)
            time = ":".join(str(time).split(".")[0].split(":")[1:])
                
            return JsonResponse({ "success": False, "message": f"You must wait {time} before you can use another hint" })

        except:
            # if no hint is used in last 5 minutes
            try:
                hint = Hints.objects.get(hint_code=code, timestamp__gte=(timezone.now() - timedelta(seconds=10)))
        
                if hint:
                    if hint.receiver:
                        return JsonResponse({ "success": False, "message": "Code has been used before" })
                        
                    if hint.creator == request.user:
                        return JsonResponse({ "success": False, "message": "You cannot use your own code" })
                    
                    # hints given to user throughout the day 
                    hints = Hints.objects.filter(receiver=request.user, word=hint.word, 
                                     timestamp__gte=timezone.now().replace(hour=0, minute=0, second=0), 
                                     timestamp__lte=timezone.now().replace(hour=23, minute=59, second=59))
                    
                    # if user used hint from the user giving them hint before
                    for hint_object in hints:
                        if hint_object.creator == hint.creator:
                            return JsonResponse({ "success": False, "message": "You cannot redeem a hint from this user again until tomorrow" })
                        
                    if hints.count() == 3:
                        return JsonResponse({ "success": False, "message": "You can only redeem 3 hints per day" })
                           
                    # use hint up                     
                    hint.receiver = request.user
                    hint.save()
                    
                    hints = list(str(hint))
                    data = []
                        
                    for letter in hints:
                        data.append({ "letter": letter, "result": Words.get_word().guess_letter(letter) })
                    return JsonResponse({ "success": True, "message": "Successfully redeemed hint", "data": data })
            except:
                return JsonResponse({ "success": False, "message": "Invalid Hint Code" })
            
    
    return None

def get_points(request):
    if request.user.is_authenticated:
        game_user = GameUser.objects.get(user=request.user)
        return JsonResponse({ "points": game_user.points, "wins": game_user.wins })

# function to calculate distance between to co-ordinates
def get_distance(first_location, second_location):
    lon1 = math.radians(first_location.longitude)
    lon2 = math.radians(second_location["longitude"])
    lat1 = math.radians(first_location.latitude)
    lat2 = math.radians(second_location["latitude"])
    
    dlon = math.copysign(lon2 - lon1, 1)
    dlat = math.copysign(lat2 - lat1, 1)
    
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6378137
    
    return c * r

def make_guess(guess):
    response = {}
    for i in range(len(guess)):
        response[i + 1] = guess[i]
        
    return response
