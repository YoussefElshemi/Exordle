from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('play/', views.play, name='play'),
    path('check/', views.check, name='check'),
    path('qr/', views.qr_code, name='qr')
]
