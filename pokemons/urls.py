# pokemons/urls.py

from django.urls import path
from . import views

app_name = 'pokemons'

urlpatterns = [
    path('', views.pokemon_list, name='list'),
    path('<int:pk>/', views.pokemon_detail, name='detail'),
    path('search/', views.pokemon_search, name='search'),
    path('custom/create/', views.create_custom_pokemon, name='create_custom'),
]