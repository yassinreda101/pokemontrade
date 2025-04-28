# trades/urls.py

from django.urls import path
from . import views

app_name = 'trades'

urlpatterns = [
    path('', views.trade_list, name='list'),
    path('<int:pk>/', views.trade_detail, name='detail'),
    path('create/', views.create_trade, name='create'),
    path('<int:pk>/respond/', views.respond_to_trade, name='respond'),
    path('<int:pk>/cancel/', views.cancel_trade, name='cancel'),
    path('add-item/<int:trade_id>/', views.add_trade_item, name='add_item'),
    path('remove-item/<int:item_id>/', views.remove_trade_item, name='remove_item'),
    path('recommendations/', views.trade_recommendations, name='recommendations'),  # Add this new URL
]