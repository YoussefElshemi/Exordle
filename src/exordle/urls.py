from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('game.urls')),
    path('admin/', admin.site.urls),
    path('microsoft/', include('microsoft_auth.urls', namespace='microsoft')),
    path('auth/', include('auth.urls')),
]
