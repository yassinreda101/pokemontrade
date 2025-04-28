# pokemon_trading_app/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('pokemons/', include('pokemons.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('trades/', include('trades.urls')),
    path('battles/', include('battles.urls')),
    path('achievements/', include('achievements.urls')),
    path('chat/', include('chat.urls')),  # Add this line
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)