# achievements/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Achievement, Badge, TrainerAchievement, TrainerBadge
from pokemons.models import Pokemon
from trades.models import Trade
from battles.models import Battle

@login_required
def achievement_list(request):
    # Get all achievements and mark which ones the user has earned
    achievements = Achievement.objects.all()
    earned_achievement_ids = TrainerAchievement.objects.filter(
        trainer=request.user
    ).values_list('achievement_id', flat=True)

    # Organize achievements by category
    achievement_categories = {}
    for achievement in achievements:
        if achievement.category not in achievement_categories:
            achievement_categories[achievement.category] = []

        # Add earned status
        achievement.is_earned = achievement.id in earned_achievement_ids
        achievement_categories[achievement.category].append(achievement)

    # Get user's achievement stats
    total_achievements = achievements.count()
    earned_achievements = len(earned_achievement_ids)
    completion_percentage = int((earned_achievements / total_achievements) * 100) if total_achievements > 0 else 0

    return render(request, 'achievements/list.html', {
        'achievement_categories': achievement_categories,
        'total_achievements': total_achievements,
        'earned_achievements': earned_achievements,
        'completion_percentage': completion_percentage,
    })

@login_required
def badge_list(request):
    # Get all badges and mark which ones the user has earned
    badges = Badge.objects.all().order_by('difficulty')
    earned_badge_ids = TrainerBadge.objects.filter(
        trainer=request.user
    ).values_list('badge_id', flat=True)

    # Add earned status to badges
    for badge in badges:
        badge.is_earned = badge.id in earned_badge_ids

    # Get user's badge stats
    total_badges = badges.count()
    earned_badges = len(earned_badge_ids)
    completion_percentage = int((earned_badges / total_badges) * 100) if total_badges > 0 else 0

    return render(request, 'achievements/badge_list.html', {
        'badges': badges,
        'total_badges': total_badges,
        'earned_badges': earned_badges,
        'completion_percentage': completion_percentage,
    })

@login_required
def achievement_progress(request):
    # Get user's statistics for achievement progress
    pokemon_count = Pokemon.objects.filter(trainer=request.user).count()
    custom_pokemon_count = Pokemon.objects.filter(trainer=request.user, is_custom=True).count()

    # Type collection progress
    collected_types = set()
    for pokemon in Pokemon.objects.filter(trainer=request.user):
        if pokemon.is_custom:
            collected_types.add(pokemon.type)
        else:
            for type_name in pokemon.species.types:
                collected_types.add(type_name)

    type_count = len(collected_types)

    # Trading progress
    trades_completed = Trade.objects.filter(
        proposer=request.user,
        status='accepted'
    ).count() + Trade.objects.filter(
        recipient=request.user,
        status='accepted'
    ).count()

    # Battle progress
    battles_won = Battle.objects.filter(
        winner=request.user
    ).count()

    # Marketplace progress
    items_sold = request.user.listings.filter(
        status='sold'
    ).count()

    return render(request, 'achievements/progress.html', {
        'pokemon_count': pokemon_count,
        'custom_pokemon_count': custom_pokemon_count,
        'type_count': type_count,
        'trades_completed': trades_completed,
        'battles_won': battles_won,
        'items_sold': items_sold,
    })