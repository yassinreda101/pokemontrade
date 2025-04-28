# pokemon_trading_app/views.py

from django.shortcuts import render
from django.db.models import Count, Q
from pokemons.models import Pokemon
from accounts.models import Trainer
from marketplace.models import MarketplaceListing
from trades.models import Trade

def home(request):
    # Get basic stats
    total_trainers = Trainer.objects.filter(is_staff=False, is_superuser=False).count()
    total_pokemon = Pokemon.objects.count()

    # Get top trainers (excluding admin/staff users)
    top_trainers = Trainer.objects.filter(is_staff=False, is_superuser=False).annotate(
        pokemon_count=Count('pokemons')
    ).order_by('-level', '-experience_points')[:5]

    # Get recent Pokemon
    recent_pokemon = Pokemon.objects.all().order_by('-acquired_date')[:4]

    # Get recent marketplace listings
    recent_listings = MarketplaceListing.objects.filter(status='active').order_by('-created_at')[:4]

    # Get recent trades
    recent_trades = Trade.objects.filter(status='accepted').order_by('-updated_at')[:5]

    context = {
        'total_trainers': total_trainers,
        'total_pokemon': total_pokemon,
        'top_trainers': top_trainers,
        'recent_pokemon': recent_pokemon,
        'recent_listings': recent_listings,
        'recent_trades': recent_trades,
    }

    return render(request, 'home.html', context)