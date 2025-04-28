# achievements/services.py

from django.db.models import Count
from .models import Achievement, Badge, TrainerAchievement, TrainerBadge

def check_achievements(trainer):
    """
    Check and grant any achievements the trainer has earned
    """
    from pokemons.models import Pokemon
    from trades.models import Trade
    from marketplace.models import MarketplaceListing
    from battles.models import Battle
    from .models import Achievement, TrainerAchievement

    # Get already earned achievements
    earned_achievement_ids = TrainerAchievement.objects.filter(
        trainer=trainer
    ).values_list('achievement_id', flat=True)

    # Get all achievements
    all_achievements = Achievement.objects.exclude(id__in=earned_achievement_ids)
    granted_achievements = []

    # Get trainer's stats
    pokemon_count = Pokemon.objects.filter(trainer=trainer).count()
    custom_pokemon_count = Pokemon.objects.filter(trainer=trainer, is_custom=True).count()

    # Get all types the trainer has
    trainer_types = set()
    for pokemon in Pokemon.objects.filter(trainer=trainer):
        if pokemon.is_custom:
            trainer_types.add(pokemon.type.lower())
        else:
            for type_name in pokemon.species.types:
                trainer_types.add(type_name.lower())

    # Trading stats
    trades_completed = Trade.objects.filter(
        proposer=trainer,
        status='accepted'
    ).count() + Trade.objects.filter(
        recipient=trainer,
        status='accepted'
    ).count()

    # Marketplace stats
    items_sold = MarketplaceListing.objects.filter(
        seller=trainer,
        status='sold'
    ).count()

    # Battle stats
    battles_won = Battle.objects.filter(
        winner=trainer
    ).count()

    # Add debugging output
    print(f"Trainer: {trainer.username}")
    print(f"Pokemon count: {pokemon_count}")
    print(f"Custom Pokemon count: {custom_pokemon_count}")
    print(f"Trainer types: {trainer_types}")
    print(f"Trades completed: {trades_completed}")
    print(f"Items sold: {items_sold}")
    print(f"Battles won: {battles_won}")

    # Check collection achievements
    if pokemon_count >= 5:
        achievement = all_achievements.filter(name='Beginner Collector').first()
        if achievement:
            TrainerAchievement.objects.create(trainer=trainer, achievement=achievement)
            granted_achievements.append(achievement)

    if pokemon_count >= 10:
        achievement = all_achievements.filter(name='Intermediate Collector').first()
        if achievement:
            TrainerAchievement.objects.create(trainer=trainer, achievement=achievement)
            granted_achievements.append(achievement)

    if pokemon_count >= 25:
        achievement = all_achievements.filter(name='Advanced Collector').first()
        if achievement:
            TrainerAchievement.objects.create(trainer=trainer, achievement=achievement)
            granted_achievements.append(achievement)

    if len(trainer_types) >= 5:
        achievement = all_achievements.filter(name='Type Enthusiast').first()
        if achievement:
            TrainerAchievement.objects.create(trainer=trainer, achievement=achievement)
            granted_achievements.append(achievement)

    if custom_pokemon_count >= 1:
        achievement = all_achievements.filter(name='Custom Creator').first()
        if achievement:
            TrainerAchievement.objects.create(trainer=trainer, achievement=achievement)
            granted_achievements.append(achievement)

    # Check trading achievements
    if trades_completed >= 1:
        achievement = all_achievements.filter(name='First Trade').first()
        if achievement:
            TrainerAchievement.objects.create(trainer=trainer, achievement=achievement)
            granted_achievements.append(achievement)

    if trades_completed >= 5:
        achievement = all_achievements.filter(name='Trading Expert').first()
        if achievement:
            TrainerAchievement.objects.create(trainer=trainer, achievement=achievement)
            granted_achievements.append(achievement)

    # Check marketplace achievements
    if items_sold >= 1:
        achievement = all_achievements.filter(name='Market Participant').first()
        if achievement:
            TrainerAchievement.objects.create(trainer=trainer, achievement=achievement)
            granted_achievements.append(achievement)

    if items_sold >= 5:
        achievement = all_achievements.filter(name='Market Mogul').first()
        if achievement:
            TrainerAchievement.objects.create(trainer=trainer, achievement=achievement)
            granted_achievements.append(achievement)

    # Check battle achievements
    if battles_won >= 1:
        achievement = all_achievements.filter(name='First Victory').first()
        if achievement:
            TrainerAchievement.objects.create(trainer=trainer, achievement=achievement)
            granted_achievements.append(achievement)
            print(f"Created First Victory achievement for {trainer.username}")

    if battles_won >= 5:
        achievement = all_achievements.filter(name='Battle Champion').first()
        if achievement:
            TrainerAchievement.objects.create(trainer=trainer, achievement=achievement)
            granted_achievements.append(achievement)

    # Special achievements
    # Achievement for earning 10 different achievements
    total_achievements = TrainerAchievement.objects.filter(trainer=trainer).count()
    if total_achievements >= 10:
        achievement = all_achievements.filter(name='Completionist').first()
        if achievement:
            TrainerAchievement.objects.create(trainer=trainer, achievement=achievement)
            granted_achievements.append(achievement)

    # Also check for badges
    check_badges(trainer)

    return granted_achievements


def check_badges(trainer):
    """
    Check and grant any badges the trainer has earned
    """
    from pokemons.models import Pokemon
    from trades.models import Trade
    from marketplace.models import MarketplaceListing
    from battles.models import Battle
    from .models import Badge, TrainerBadge

    # Get already earned badges
    earned_badge_ids = TrainerBadge.objects.filter(
        trainer=trainer
    ).values_list('badge_id', flat=True)

    # Get all badges
    all_badges = Badge.objects.exclude(id__in=earned_badge_ids)
    granted_badges = []

    # Always grant starter badge to new trainers
    starter_badge = all_badges.filter(name='Starter Badge').first()
    if starter_badge:
        TrainerBadge.objects.create(trainer=trainer, badge=starter_badge)
        granted_badges.append(starter_badge)

    # Get trainer's stats
    pokemon_count = Pokemon.objects.filter(trainer=trainer).count()
    custom_pokemon_count = Pokemon.objects.filter(trainer=trainer, is_custom=True).count()

    # Get all types the trainer has
    trainer_types = set()
    for pokemon in Pokemon.objects.filter(trainer=trainer):
        if pokemon.is_custom:
            trainer_types.add(pokemon.type.lower())
        else:
            for type_name in pokemon.species.types:
                trainer_types.add(type_name.lower())

    # Trading stats
    trades_completed = Trade.objects.filter(
        proposer=trainer,
        status='accepted'
    ).count() + Trade.objects.filter(
        recipient=trainer,
        status='accepted'
    ).count()

    # Marketplace stats
    items_sold = MarketplaceListing.objects.filter(
        seller=trainer,
        status='sold'
    ).count()

    # Battle stats
    battles_won = Battle.objects.filter(
        winner=trainer
    ).count()

    # Add debugging output
    print(f"Checking badges for: {trainer.username}")
    print(f"Pokemon count: {pokemon_count}")
    print(f"Custom Pokemon count: {custom_pokemon_count}")
    print(f"Trainer types: {trainer_types}")
    print(f"Trades completed: {trades_completed}")
    print(f"Items sold: {items_sold}")
    print(f"Battles won: {battles_won}")
    print(f"Trainer level: {trainer.level}")

    # Check for Collection Badge
    if pokemon_count >= 10:
        badge = all_badges.filter(name='Collection Badge').first()
        if badge:
            TrainerBadge.objects.create(trainer=trainer, badge=badge)
            granted_badges.append(badge)
            print(f"Granted Collection Badge to {trainer.username}")

    # Check for Diversity Badge
    if len(trainer_types) >= 8:
        badge = all_badges.filter(name='Diversity Badge').first()
        if badge:
            TrainerBadge.objects.create(trainer=trainer, badge=badge)
            granted_badges.append(badge)
            print(f"Granted Diversity Badge to {trainer.username}")

    # Check for Trading Badge
    if trades_completed >= 5:
        badge = all_badges.filter(name='Trading Badge').first()
        if badge:
            TrainerBadge.objects.create(trainer=trainer, badge=badge)
            granted_badges.append(badge)
            print(f"Granted Trading Badge to {trainer.username}")

    # Check for Battle Badge
    if battles_won >= 5:
        badge = all_badges.filter(name='Battle Badge').first()
        if badge:
            TrainerBadge.objects.create(trainer=trainer, badge=badge)
            granted_badges.append(badge)
            print(f"Granted Battle Badge to {trainer.username}")

    # Check for Custom Creator Badge
    if custom_pokemon_count >= 3:
        badge = all_badges.filter(name='Custom Creator Badge').first()
        if badge:
            TrainerBadge.objects.create(trainer=trainer, badge=badge)
            granted_badges.append(badge)
            print(f"Granted Custom Creator Badge to {trainer.username}")

    # Check for Marketplace Badge
    if items_sold >= 5:
        badge = all_badges.filter(name='Marketplace Badge').first()
        if badge:
            TrainerBadge.objects.create(trainer=trainer, badge=badge)
            granted_badges.append(badge)
            print(f"Granted Marketplace Badge to {trainer.username}")

    # Check for Elite Trainer Badge
    if trainer.level >= 10:
        badge = all_badges.filter(name='Elite Trainer Badge').first()
        if badge:
            TrainerBadge.objects.create(trainer=trainer, badge=badge)
            granted_badges.append(badge)
            print(f"Granted Elite Trainer Badge to {trainer.username}")

    return granted_badges