from datetime import datetime
import random
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

    return render(request, 'game/index.html', context)

def play(request):
    if request.user.is_authenticated:
        word = str(Words.get_word())
        guesses = Guesses.objects.filter(user=request.user, word=word, day_of_guess=datetime.now())
        
        length = len(word) + 1

        context = {
            'user': request.user,
            'guesses': guesses,
            'word_range': range(1, length),
            'guess_range': range(1, length + 1)
        }

        return render(request, 'game/play.html', context)

    return redirect('/auth/login')

def check(request):
    if request.method == 'POST' and request.user.is_authenticated:
        word = Words.get_word()
        data = word.guess(request, request.POST.dict())
        
        return JsonResponse(data)

    return None

def qr_code(request):
    if request.method == 'POST':
        code = str(random.randint(0, 999999))
        padded_code = code.zfill(6)

        factory = qrcode.image.svg.SvgPathImage
        img = qrcode.make(padded_code, image_factory=factory, box_size=20)
        stream = BytesIO()
        img.save(stream)

        return JsonResponse({ 'svg': stream.getvalue().decode() })

    return None
