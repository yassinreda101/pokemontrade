# achievements/urls.py

from django.urls import path
from . import views

app_name = 'achievements'

urlpatterns = [
    path('', views.achievement_list, name='list'),
    path('badges/', views.badge_list, name='badge_list'),
    path('progress/', views.achievement_progress, name='progress'),
]