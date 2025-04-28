# marketplace/urls.py

from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.listing_list, name='list'),
    path('<int:pk>/', views.listing_detail, name='detail'),
    path('create/', views.create_listing, name='create'),
    path('purchase/<int:pk>/', views.purchase_listing, name='purchase'),
    path('cancel/<int:pk>/', views.cancel_listing, name='cancel'),
    path('delete/<int:pk>/', views.delete_listing, name='delete'),
]