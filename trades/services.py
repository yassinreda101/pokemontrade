# trades/services.py

import random
from django.db.models import Count, Avg, Q
from pokemons.models import Pokemon, PokemonSpecies

def get_trade_recommendations(trainer):
    """
    Generate AI trade recommendations for a trainer - SQLite compatible version
    """
    recommendations = {
        'missing_types': [],
        'rare_pokemon': [],
        'complementary_pokemon': [],
        'popular_pokemon': [],
        'explanation': ''
    }

    # Get trainer's Pokemon
    trainer_pokemon = Pokemon.objects.filter(trainer=trainer)

    if not trainer_pokemon.exists():
        return {
            'explanation': "You don't have any Pokemon yet. Get some starter Pokemon first!"
        }

    # 1. Find missing types in trainer's collection
    trainer_types = set()
    for pokemon in trainer_pokemon:
        if pokemon.is_custom:
            trainer_types.add(pokemon.type.lower())
        else:
            for type_name in pokemon.species.types:
                trainer_types.add(type_name.lower())

    all_types = {
        'normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting',
        'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost',
        'dragon', 'dark', 'steel', 'fairy'
    }

    missing_types = all_types - trainer_types

    if missing_types:
        # Find Pokemon of missing types that other trainers have
        for type_name in list(missing_types)[:3]:  # Limit to 3 missing types
            # Find Pokemon with this type owned by other trainers
            type_pokemon = None
            if Pokemon.objects.filter(~Q(trainer=trainer), Q(type__icontains=type_name)).exists():
                # For custom Pokemon
                type_pokemon = Pokemon.objects.filter(
                    ~Q(trainer=trainer),
                    Q(type__icontains=type_name)
                ).first()
            else:
                # For regular Pokemon, we need to iterate through all Pokemon species
                # This is less efficient but works with SQLite
                all_species = PokemonSpecies.objects.all()
                species_with_type = []

                for species in all_species:
                    if type_name in (t.lower() for t in species.types):
                        species_with_type.append(species.id)

                if species_with_type:
                    type_pokemon = Pokemon.objects.filter(
                        ~Q(trainer=trainer),
                        Q(species_id__in=species_with_type)
                    ).first()

            if type_pokemon:
                recommendations['missing_types'].append({
                    'pokemon': type_pokemon,
                    'reason': f"You don't have any {type_name.title()} type Pokemon"
                })

    # 2. Find rare Pokemon the trainer doesn't have
    rare_pokemon = Pokemon.objects.filter(
        ~Q(trainer=trainer),
        Q(rarity__in=['rare', 'legendary'])
    ).order_by('?')[:2]  # Random selection of 2 rare Pokemon

    for pokemon in rare_pokemon:
        recommendations['rare_pokemon'].append({
            'pokemon': pokemon,
            'reason': f"This is a {pokemon.get_rarity_display()} Pokemon that would be valuable in your collection"
        })

    # 3. Find Pokemon that complement the trainer's highest level Pokemon
    highest_level_pokemon = trainer_pokemon.order_by('-level').first()
    if highest_level_pokemon:
        # Find complementary types (e.g., if trainer has Fire, suggest Water or Grass)
        complementary_types = []

        if highest_level_pokemon.is_custom:
            primary_type = highest_level_pokemon.type.lower()
        else:
            primary_type = highest_level_pokemon.species.types[0].lower() if highest_level_pokemon.species.types else 'normal'

        # Type effectiveness mapping (simplified)
        type_complements = {
            'fire': ['water', 'ground', 'rock'],
            'water': ['electric', 'grass'],
            'grass': ['fire', 'ice', 'flying', 'bug'],
            'electric': ['ground'],
            'ice': ['fire', 'fighting', 'rock', 'steel'],
            'fighting': ['flying', 'psychic', 'fairy'],
            'poison': ['ground', 'psychic'],
            'ground': ['water', 'grass', 'ice'],
            'flying': ['electric', 'ice', 'rock'],
            'psychic': ['bug', 'ghost', 'dark'],
            'bug': ['fire', 'flying', 'rock'],
            'rock': ['water', 'grass', 'fighting', 'ground', 'steel'],
            'ghost': ['ghost', 'dark'],
            'dragon': ['ice', 'dragon', 'fairy'],
            'dark': ['fighting', 'bug', 'fairy'],
            'steel': ['fire', 'fighting', 'ground'],
            'fairy': ['poison', 'steel'],
            'normal': ['fighting']
        }

        complementary_types = type_complements.get(primary_type, ['fire', 'water', 'electric'])  # Default to basic types

        # Find Pokemon of complementary types
        for comp_type in complementary_types[:2]:  # Limit to 2 complementary types
            comp_pokemon = None

            # Check custom Pokemon first
            if Pokemon.objects.filter(~Q(trainer=trainer), Q(type__icontains=comp_type)).exists():
                comp_pokemon = Pokemon.objects.filter(
                    ~Q(trainer=trainer),
                    Q(type__icontains=comp_type)
                ).first()
            else:
                # For regular Pokemon, iterate through all species
                all_species = PokemonSpecies.objects.all()
                species_with_type = []

                for species in all_species:
                    if comp_type in (t.lower() for t in species.types):
                        species_with_type.append(species.id)

                if species_with_type:
                    comp_pokemon = Pokemon.objects.filter(
                        ~Q(trainer=trainer),
                        Q(species_id__in=species_with_type)
                    ).first()

            if comp_pokemon:
                recommendations['complementary_pokemon'].append({
                    'pokemon': comp_pokemon,
                    'reason': f"This {comp_type.title()} type Pokemon would complement your {highest_level_pokemon.display_name}"
                })

    # 4. Find popular Pokemon among other trainers
    popular_pokemon = Pokemon.objects.values('species_id').annotate(
        count=Count('id')
    ).filter(
        count__gt=1,  # Pokemon that multiple trainers have
        species_id__isnull=False  # Exclude custom Pokemon
    ).order_by('-count')[:3]

    for pop in popular_pokemon:
        # Check if trainer already has this Pokemon
        if not trainer_pokemon.filter(species_id=pop['species_id']).exists():
            species = PokemonSpecies.objects.get(id=pop['species_id'])
            example_pokemon = Pokemon.objects.filter(
                ~Q(trainer=trainer),
                species_id=pop['species_id']
            ).first()

            if example_pokemon:
                recommendations['popular_pokemon'].append({
                    'pokemon': example_pokemon,
                    'reason': f"{species.name.title()} is popular among trainers"
                })

    # Generate an explanation based on the trainer's collection
    if trainer_pokemon.count() < 5:
        recommendations['explanation'] = "You're just starting your collection. Try to acquire more diverse Pokemon types!"
    elif missing_types:
        recommendations['explanation'] = f"Your collection is missing {len(missing_types)} Pokemon types. Trading for these types would make your collection more balanced!"
    else:
        recommendations['explanation'] = "You have a diverse collection! Focus on trading for rare Pokemon or those that complement your strongest Pokemon."

    return recommendations