from datetime import datetime
import random
import math
from io import BytesIO
import qrcode
import qrcode.image.svg
from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import Guesses, Words

def index(request):
    context = {
        'user': request.user
    }

    # push user object to front-end
    return render(request, 'game/index.html', context)

def play(request):
    # only accessible if user is logged in
    if request.user.is_authenticated:
        
        # get word of the day and previous guesses for this word if there are any
        word = Words.get_word()
        guesses = Guesses.objects.filter(user=request.user, word=word, day_of_guess=datetime.now())      
          
        length = len(str(word)) + 1

        context = {
            'user': request.user,
            'guesses': guesses,
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
        
        return JsonResponse(data)

    return None

def qr_code(request):
    if request.method == 'POST':
        
        # generate a random 6 digit code
        code = str(random.randint(0, 999999))
        padded_code = code.zfill(6)

        # generate and return SVG for QR code representing the 6 digit code
        factory = qrcode.image.svg.SvgPathImage
        img = qrcode.make(padded_code, image_factory=factory, box_size=20)
        stream = BytesIO()
        img.save(stream)

        return JsonResponse({ 'svg': stream.getvalue().decode() })

    return None

def check_in(request):
    if request.method == "POST":
        # get word of the day's location
        first_location = Words.get_word().location
        
        second_location = {
            "latitude": float(request.POST.get("latitude")),
            "longitude": float(request.POST.get("longitude"))
        }
               
        # calcuate distance between user's current location and the word's location                                 
        distance = get_distance(first_location, second_location)
                
        # if they are within the the radius                
        if (distance < first_location.radius):
            return JsonResponse({ "success": True }) 
        else:
            return JsonResponse({ "success": False, "distance": distance - first_location.radius })
        
    return None

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