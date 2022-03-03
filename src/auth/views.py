from django.shortcuts import redirect
from django.contrib.auth import logout as signout

# redirect user to microsoft auth page, 
# then once they login, redirect to /play
def login(request):
    return redirect('/microsoft/to-auth-redirect/?next=play')

# log user out then redirect to home page
def logout(request):
    signout(request)
    return redirect('/')
