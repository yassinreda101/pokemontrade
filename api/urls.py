# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

router = DefaultRouter()
# These will be implemented when we create the viewsets
# router.register(r'trainers', views.TrainerViewSet)
# router.register(r'pokemons', views.PokemonViewSet)
# router.register(r'marketplace', views.MarketplaceViewSet)
# router.register(r'trades', views.TradeViewSet)
# router.register(r'battles', views.BattleViewSet)
# router.register(r'achievements', views.AchievementViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('battle/ai/', views.ai_battle, name='ai_battle'),
    # path('pokemon/generate/', views.generate_pokemon, name='generate_pokemon'),
]