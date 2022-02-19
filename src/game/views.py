import json
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'game/index.html', {})

def game(request):
    word = 'FORUM'
    length = len(word) + 1

    context = {
      'word_range': range(1, length),
      'range': range(1, length + 1)
    }

    return render(request, 'game/play.html', context)

def check(request):
    word = 'FORUM'
    request.POST._mutable = True

    request.POST.pop("guess")
    request.POST.pop("csrfmiddlewaretoken")

    request.POST._mutable = False

    data = {}
    for position, value in request.POST.items():
        idx = int(position) - 1
        if word[idx] == value.upper():
            data[position] = "perfect"
            word = word.replace(value.upper(), " ")
        elif value.upper() in word:
            data[position] = "correct"
            word = word.replace(value.upper(), " ")
        else:
            data[position] = "wrong"

    return HttpResponse(json.dumps(data))
 