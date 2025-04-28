# chat/urls.py

from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('room/<str:room_name>/', views.room, name='room'),
    path('create/', views.create_room, name='create_room'),
]