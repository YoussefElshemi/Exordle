from django.http import JsonResponse
from django.shortcuts import render

from game.models import Words

def index(request):
    return render(request, 'map/index.html')

def search(request):
  # only accessible if user is logged in
    if request.user.is_authenticated:
        try: 
            word = Words.objects.get(word=request.POST.get("search").upper())
            location = word.location
            
            return JsonResponse({ "success": True, "lng": location.longitude, "lat": location.latitude })
        except:
            return JsonResponse({ "success": False, "message": "Word is not valid" })
    return None