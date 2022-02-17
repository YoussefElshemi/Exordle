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