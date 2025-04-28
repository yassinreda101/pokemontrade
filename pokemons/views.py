# pokemons/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Pokemon, PokemonSpecies
from .forms import PokemonSearchForm, CustomPokemonForm
from .services import generate_pokemon_image, fetch_pokemon_from_pokeapi
from pokemon_trading_app.factories import CustomPokemonFactory

@login_required
def pokemon_list(request):
    # Get user's Pokemon
    pokemons = Pokemon.objects.filter(trainer=request.user)

    # Process search form
    form = PokemonSearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data.get('query')
        type_filter = form.cleaned_data.get('type_filter')
        rarity_filter = form.cleaned_data.get('rarity_filter')

        # Apply filters
        if query:
            pokemons = pokemons.filter(
                Q(nickname__icontains=query) |
                Q(species__name__icontains=query) |
                Q(name__icontains=query)
            )

        if type_filter:
            # Filter by type field (for custom Pokemon with type field)
            type_filter_pokemons = pokemons.filter(type__icontains=type_filter)

            # Combine with species type filtering (for regular Pokemon)
            species_with_type = [p.id for p in pokemons if p.species and type_filter in p.species.types]
            species_type_pokemons = pokemons.filter(id__in=species_with_type)

            # Combine both querysets
            pokemons = type_filter_pokemons | species_type_pokemons

        if rarity_filter:
            pokemons = pokemons.filter(rarity=rarity_filter)

    return render(request, 'pokemons/list.html', {
        'pokemons': pokemons,
        'form': form
    })

@login_required
def pokemon_detail(request, pk):
    pokemon = get_object_or_404(Pokemon, pk=pk, trainer=request.user)
    return render(request, 'pokemons/detail.html', {'pokemon': pokemon})

@login_required
def pokemon_search(request):
    results = []
    query = request.GET.get('query', '')
    popular_pokemon = []

    if query:
        # Search for Pokemon in the database
        results = PokemonSpecies.objects.filter(name__icontains=query)[:12]

        # If no results in database, try fetching from API
        if not results:
            try:
                # Try fetching by name or ID
                pokemon_data = fetch_pokemon_from_pokeapi(query.lower())
                if pokemon_data:
                    # Extract types
                    types = [t['type']['name'] for t in pokemon_data['types']]

                    # Extract abilities
                    abilities = [a['ability']['name'] for a in pokemon_data['abilities']]

                    # Extract stats
                    stats = {s['stat']['name']: s['base_stat'] for s in pokemon_data['stats']}

                    # Create or get the species
                    species, created = PokemonSpecies.objects.get_or_create(
                        api_id=pokemon_data['id'],
                        defaults={
                            'name': pokemon_data['name'],
                            'types': types,
                            'height': pokemon_data['height'],
                            'weight': pokemon_data['weight'],
                            'abilities': abilities,
                            'base_experience': pokemon_data['base_experience'],
                            'stats': stats,
                            'image_url': pokemon_data['sprites']['other']['official-artwork']['front_default']
                        }
                    )
                    results = [species]
            except:
                pass
    else:
        # Show 4 popular starter Pokemon by default
        popular_ids = [25, 1, 4, 7]  # Pikachu, Bulbasaur, Charmander, Squirtle

        # Try to get species from database first
        db_species = PokemonSpecies.objects.filter(api_id__in=popular_ids)
        popular_pokemon.extend(db_species)

        # For any missing starters, try to fetch from API
        fetched_ids = [s.api_id for s in db_species]
        for pokemon_id in popular_ids:
            if pokemon_id not in fetched_ids:
                try:
                    species = PokemonSpecies.fetch_from_api(pokemon_id)
                    if species:
                        popular_pokemon.append(species)
                except:
                    pass

    return render(request, 'pokemons/search.html', {
        'results': results,
        'query': query,
        'popular_pokemon': popular_pokemon,
    })

@login_required
def create_custom_pokemon(request):
    if request.method == 'POST':
        form = CustomPokemonForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            type_name = form.cleaned_data['type']

            # Generate image URL
            image_url = generate_pokemon_image(name, type_name)

            # Create the Pokemon using factory
            factory = CustomPokemonFactory()
            pokemon = factory.create_pokemon(request.user, name, type_name)

            # Check achievements and badges after creating custom Pokemon
            from achievements.services import check_achievements
            check_achievements(request.user)

            messages.success(request, f'Your custom Pokemon {name} has been created!')
            return redirect('pokemons:detail', pk=pokemon.id)
    else:
        form = CustomPokemonForm()

    return render(request, 'pokemons/create_custom.html', {'form': form})