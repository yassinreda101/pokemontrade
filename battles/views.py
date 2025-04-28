# battles/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import random
import json
from django.db.models import Q
from .models import Battle, BattlePokemon
from .forms import BattleAIForm, BattlePlayerForm
from pokemons.models import Pokemon
from pokemons.services import generate_ai_battle_log, fetch_pokemon_cards

@login_required
def battle_list(request):
    # Get user's battles
    battles_as_challenger = Battle.objects.filter(challenger=request.user).order_by('-created_at')
    battles_as_opponent = Battle.objects.filter(opponent=request.user).order_by('-created_at')

    # Process battle results for display
    for battle in battles_as_challenger:
        if battle.status == 'completed':
            if battle.is_ai_opponent and isinstance(battle.battle_log, dict):
                # Handle AI battle results
                if battle.battle_log.get('winner') == 'Challenger':
                    battle.result_display = 'Victory'
                elif battle.battle_log.get('winner') == 'AI':
                    battle.result_display = 'Defeat'
                else:
                    battle.result_display = 'Draw'
            else:
                # Handle player battle results
                if battle.winner == request.user:
                    battle.result_display = 'Victory'
                elif battle.winner and battle.winner != request.user:
                    battle.result_display = 'Defeat'
                else:
                    battle.result_display = 'Draw'
        else:
            battle.result_display = '-'

    # Process battle results for opponent battles
    for battle in battles_as_opponent:
        if battle.status == 'completed':
            if battle.winner == request.user:
                battle.result_display = 'Victory'
            elif battle.winner and battle.winner != request.user:
                battle.result_display = 'Defeat'
            else:
                battle.result_display = 'Draw'
        else:
            battle.result_display = '-'

    return render(request, 'battles/list.html', {
        'battles_as_challenger': battles_as_challenger,
        'battles_as_opponent': battles_as_opponent,
    })

@login_required
def battle_detail(request, pk):
    # Get battle and make sure user is involved
    if Battle.objects.filter(pk=pk, challenger=request.user).exists():
        battle = get_object_or_404(Battle, pk=pk, challenger=request.user)
    else:
        battle = get_object_or_404(Battle, pk=pk, opponent=request.user)

    # Get battle Pokemon
    challenger_pokemon = BattlePokemon.objects.filter(battle=battle, trainer=battle.challenger).first()
    opponent_pokemon = None
    opponent_pokemon_name = None
    ai_pokemon_type = None
    ai_pokemon_image = None
    ai_hp_percent = 100
    challenger_hp_percent = 100

    # For AI battles, get the AI Pokemon name from the battle log if available
    if battle.is_ai_opponent:
        if battle.battle_log and isinstance(battle.battle_log, dict):
            # Get AI Pokemon details
            if 'ai_pokemon_name' in battle.battle_log:
                opponent_pokemon_name = battle.battle_log['ai_pokemon_name']
            if 'ai_pokemon_type' in battle.battle_log:
                ai_pokemon_type = battle.battle_log['ai_pokemon_type']
            # Get HP percentages
            if 'ai_hp' in battle.battle_log:
                ai_hp_percent = battle.battle_log['ai_hp']
            if 'challenger_hp' in battle.battle_log:
                challenger_hp_percent = battle.battle_log['challenger_hp']
                # Update the challenger_pokemon object with the correct HP
                if challenger_pokemon:
                    challenger_pokemon.current_hp = challenger_hp_percent
                    challenger_pokemon.save()

        # If still None, use a default
        if not opponent_pokemon_name:
            ai_pokemon_names = [
                "Charizard", "Blastoise", "Venusaur", "Pikachu", "Gyarados",
                "Gengar", "Dragonite", "Tyranitar", "Metagross", "Garchomp"
            ]
            opponent_pokemon_name = random.choice(ai_pokemon_names)

        # Try to get a TCG API image for this Pokemon
        pokemon_cards = fetch_pokemon_cards(opponent_pokemon_name, 1)
        if pokemon_cards and len(pokemon_cards) > 0:
            # Get the image from the first card
            ai_pokemon_image = pokemon_cards[0].get('images', {}).get('small')
    else:
        # For player battles
        opponent_pokemon = BattlePokemon.objects.filter(battle=battle, trainer=battle.opponent).first()

    # Parse battle log
    battle_log = battle.battle_log

    # Get battle result (fix the incorrect draw result)
    battle_result = None
    if battle.status == 'completed':
        if battle.is_ai_opponent and isinstance(battle.battle_log, dict):
            if battle.battle_log.get('winner') == 'Draw':
                battle_result = 'Draw'
            elif battle.battle_log.get('winner') == 'Challenger' and battle.challenger == request.user:
                battle_result = 'Victory'
            elif battle.battle_log.get('winner') == 'AI':
                battle_result = 'Defeat'
        elif battle.winner == request.user:
            battle_result = 'Victory'
        elif battle.winner and battle.winner != request.user:
            battle_result = 'Defeat'
        elif not battle.winner:
            battle_result = 'Draw'

    return render(request, 'battles/detail.html', {
        'battle': battle,
        'challenger_pokemon': challenger_pokemon,
        'opponent_pokemon': opponent_pokemon,
        'opponent_pokemon_name': opponent_pokemon_name,
        'ai_pokemon_type': ai_pokemon_type,
        'ai_hp_percent': ai_hp_percent,
        'challenger_hp_percent': challenger_hp_percent,  # Added this variable
        'battle_log': battle_log,
        'ai_pokemon_image': ai_pokemon_image,
        'battle_result': battle_result,
    })

@login_required
def create_ai_battle(request):
    # Check if Pokemon ID was passed in the URL
    pokemon_id = request.GET.get('pokemon')
    initial_data = {}

    if pokemon_id:
        try:
            pokemon = Pokemon.objects.get(id=pokemon_id, trainer=request.user)
            initial_data['pokemon'] = pokemon
        except Pokemon.DoesNotExist:
            pass

    if request.method == 'POST':
        form = BattleAIForm(request.POST, user=request.user)
        if form.is_valid():
            pokemon = form.cleaned_data['pokemon']

            # Create battle
            battle = Battle.objects.create(
                challenger=request.user,
                is_ai_opponent=True,
                status='in_progress'
            )

            # Add challenger's Pokemon to battle
            challenger_battle_pokemon = BattlePokemon.objects.create(
                battle=battle,
                pokemon=pokemon,
                trainer=request.user,
                current_hp=pokemon.stats.get('hp', 100) if not pokemon.is_custom else 100
            )

            # Generate battle with AI - select a well-known Pokemon
            ai_pokemon_name = random.choice([
                "Charizard", "Blastoise", "Venusaur", "Pikachu", "Gyarados",
                "Gengar", "Dragonite", "Tyranitar", "Metagross", "Garchomp"
            ])

            # Try to get a TCG API image for this Pokemon
            pokemon_cards = fetch_pokemon_cards(ai_pokemon_name, 1)
            ai_pokemon_image = None

            if pokemon_cards and len(pokemon_cards) > 0:
                # Get the image from the first card
                ai_pokemon_image = pokemon_cards[0].get('images', {}).get('small')

            # Simulate battle
            battle_result = generate_ai_battle_log(pokemon, ai_pokemon_name)

            # Add TCG image to battle results if available
            if ai_pokemon_image:
                battle_result['ai_pokemon_image'] = ai_pokemon_image

            # Update battle with results
            battle.battle_log = battle_result
            battle.status = 'completed'
            battle.completed_at = timezone.now()

            # Set winner based on the battle result
            if battle_result.get('winner') == 'Challenger':
                battle.winner = request.user
                # Grant XP to winner
                request.user.increase_xp(100)
                pokemon.experience += 50
                pokemon.save()
            elif battle_result.get('winner') == 'AI':
                battle.winner = None  # No trainer is the winner if AI wins
            else:
                # It's a draw
                battle.winner = None

            battle.save()

            # Check for achievements after battle
            from achievements.services import check_achievements
            check_achievements(request.user)

            messages.success(request, "Battle completed! Check the results!")
            return redirect('battles:detail', pk=battle.pk)
    else:
        form = BattleAIForm(user=request.user, initial=initial_data)

    return render(request, 'battles/create_ai.html', {'form': form})

@login_required
def create_player_battle(request):
    if request.method == 'POST':
        form = BattlePlayerForm(request.POST, user=request.user)
        if form.is_valid():
            opponent = form.cleaned_data['opponent']
            pokemon = form.cleaned_data['pokemon']

            # Create battle (pending for now)
            battle = Battle.objects.create(
                challenger=request.user,
                opponent=opponent,
                is_ai_opponent=False,
                status='pending'
            )

            # Add challenger's Pokemon to battle
            challenger_battle_pokemon = BattlePokemon.objects.create(
                battle=battle,
                pokemon=pokemon,
                trainer=request.user,
                current_hp=pokemon.stats.get('hp', 100) if not pokemon.is_custom else 100
            )

            messages.success(request, f"Battle challenge sent to {opponent.username}!")
            return redirect('battles:detail', pk=battle.pk)
    else:
        form = BattlePlayerForm(user=request.user)

    return render(request, 'battles/create_player.html', {'form': form})

@login_required
def respond_to_battle(request, pk):
    battle = get_object_or_404(Battle, pk=pk, opponent=request.user, status='pending')

    if request.method == 'POST':
        pokemon_id = request.POST.get('pokemon')

        if not pokemon_id:
            messages.error(request, "Please select a Pokemon for battle!")
            return redirect('battles:detail', pk=battle.pk)

        try:
            pokemon = Pokemon.objects.get(id=pokemon_id, trainer=request.user)

            # Add Pokemon to battle and simulate
            success, message = battle.respond_to_challenge(pokemon)

            if success:
                messages.success(request, message)

                # Check for achievements
                from achievements.services import check_achievements
                check_achievements(request.user)
                check_achievements(battle.challenger)
            else:
                messages.error(request, message)

        except Pokemon.DoesNotExist:
            messages.error(request, "Invalid Pokemon selection!")

    return redirect('battles:detail', pk=battle.pk)