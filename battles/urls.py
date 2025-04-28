# battles/urls.py

from django.urls import path
from . import views

app_name = 'battles'

urlpatterns = [
    path('', views.battle_list, name='list'),
    path('<int:pk>/', views.battle_detail, name='detail'),
    path('create/ai/', views.create_ai_battle, name='create_ai'),
    path('create/player/', views.create_player_battle, name='create_player'),
    path('<int:pk>/respond/', views.respond_to_battle, name='respond'),
]