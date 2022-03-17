from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('play/', views.play, name='play'),
    path('check/', views.check, name='check'),
    path('qr/', views.qr_code, name='qr'),
    path('check_in/', views.check_in, name='check_in'),
    path('hint/', views.hint, name='hint')
]
