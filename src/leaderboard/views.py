from django.shortcuts import render

from auth.models import GameUser

def index(request):
    game_users = GameUser.objects.filter(points__gte=1).order_by('points').reverse()
    users = []
    
    for game_user in game_users:
      if game_user.user.first_name:
        username = f"{game_user.user.first_name} {game_user.user.last_name} ({game_user.user.username.split('@')[0]})"
      else:
        username = game_user.user.username
        
      users.append({ "username": username, "points": game_user.points })
    
    context = {
      'users': users
    }
    
    return render(request, 'leaderboard/index.html', context)
