from django.shortcuts import redirect
from django.contrib.auth import logout as signout

def login(request):
    if request:
        response = redirect('/microsoft/to-auth-redirect/?next=play')
        return response
    
    return None

def logout(request):
    signout(request)
    response = redirect('/')
    return response
