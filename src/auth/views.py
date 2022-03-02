from django.shortcuts import redirect
from django.contrib.auth import logout as signout

def login(request):
    return redirect('/microsoft/to-auth-redirect/?next=play')

def logout(request):
    signout(request)
    return redirect('/')
