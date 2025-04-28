# pokemons/services.py

import requests
import json
import os
import uuid
from api.models import APILog
import random
from django.conf import settings

def fetch_pokemon_from_pokeapi(pokemon_id):
    """
    Fetch Pokemon data from PokeAPI
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"

    try:
        response = requests.get(url)

        # Log the API request
        APILog.objects.create(
            api_name='pokeapi',
            endpoint=url,
            response_status=response.status_code,
            response_data=response.json() if response.status_code == 200 else None
        )

        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        # Log error
        APILog.objects.create(
            api_name='pokeapi',
            endpoint=url,
            response_status=500,
            response_data={'error': str(e)}
        )
        return None

def fetch_pokemon_cards(pokemon_name=None, limit=10):
    """
    Fetch Pokemon cards from Pokemon TCG API
    """
    url = "https://api.pokemontcg.io/v2/cards"
    params = {'pageSize': limit}
    headers = {}

    # Add API key if available
    if settings.POKEMONTCG_API_KEY:
        headers['X-Api-Key'] = settings.POKEMONTCG_API_KEY

    # Add name filter if provided
    if pokemon_name:
        params['q'] = f'name:{pokemon_name}'

    try:
        response = requests.get(url, params=params, headers=headers)

        # Log the API request
        from api.models import APILog
        APILog.objects.create(
            api_name='pokemontcg',
            endpoint=url,
            request_data=params,
            response_status=response.status_code,
            response_data=response.json() if response.status_code == 200 else None
        )

        if response.status_code == 200:
            return response.json().get('data', [])
        return []
    except Exception as e:
        # Log error
        from api.models import APILog
        APILog.objects.create(
            api_name='pokemontcg',
            endpoint=url,
            request_data=params,
            response_status=500,
            response_data={'error': str(e)}
        )
        return []

def generate_pokemon_image(name, type_name):
    """
    Generate a custom Pokemon image using DALL-E
    """
    try:
        import openai
        import requests
        import os
        import uuid
        from api.models import APILog

        if not settings.OPENAI_API_KEY:
            # Return a placeholder image URL if no API key is available
            return f"https://via.placeholder.com/512x512.png?text={name}+({type_name})"

        # Set the API key from settings
        openai.api_key = settings.OPENAI_API_KEY

        # OpenAI API has changed - update to use the new client
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

        # Improved prompt for better results
        prompt = f"Create a pixel art style image of a fictional monster named '{name}' of type {type_name}. The creature should clearly reflect its name '{name}' in its design and appearance. Use a clean white background with no text or other elements. Make it cute and colorful, showing the full body of the monster in a centered position."

        # Generate image using DALL-E
        print(f"Generating image for Pokemon: {name} of type {type_name}")
        response = client.images.generate(
            model="dall-e-3", # or "dall-e-2" based on your preference
            prompt=prompt,
            n=1,
            size="1024x1024" # or "512x512" for DALL-E 2
        )

        # Log the API request
        APILog.objects.create(
            api_name='openai',
            endpoint='images.generate',
            request_data={'type': 'pokemon_generation', 'prompt': prompt},
            response_status=200,
            response_data={'success': True}
        )

        # Get the image URL from the response
        image_url = response.data[0].url
        print(f"Image URL received from OpenAI: {image_url}")

        # Download the image
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            # Create media directory if it doesn't exist
            media_path = os.path.join(settings.MEDIA_ROOT, 'pokemon_images')
            os.makedirs(media_path, exist_ok=True)
            print(f"Media directory path: {media_path}")

            # Save the image to disk
            img_filename = f"{name.lower()}_{uuid.uuid4().hex}.png"
            img_path = os.path.join(media_path, img_filename)

            with open(img_path, 'wb') as f:
                f.write(img_response.content)

            # Debug info
            print(f"Image saved to: {img_path}")

            # The correct URL path for Django to serve
            return f"{settings.MEDIA_URL}pokemon_images/{img_filename}"

        # If download fails, return the OpenAI URL directly
        print("Failed to download image, returning direct OpenAI URL")
        return image_url

    except Exception as e:
        # Log error
        from api.models import APILog
        APILog.objects.create(
            api_name='openai',
            endpoint='images.generate',
            request_data={'type': 'pokemon_generation'},
            response_status=500,
            response_data={'error': str(e)}
        )
        print(f"Error generating image: {str(e)}")
        # Return a placeholder image URL on error
        return f"https://via.placeholder.com/512x512.png?text={name}+({type_name})"

def generate_ai_battle_log(challenger_pokemon, ai_pokemon_name):
    """
    Generate an AI battle log with more realistic outcomes
    """
    # Pokemon moves based on types
    moves_by_type = {
        'normal': ['Tackle', 'Quick Attack', 'Body Slam', 'Hyper Beam'],
        'fire': ['Ember', 'Flamethrower', 'Fire Blast', 'Inferno'],
        'water': ['Water Gun', 'Bubble Beam', 'Hydro Pump', 'Aqua Jet'],
        'electric': ['Thunder Shock', 'Thunderbolt', 'Thunder', 'Volt Tackle'],
        'grass': ['Vine Whip', 'Razor Leaf', 'Solar Beam', 'Leaf Storm'],
        'ice': ['Ice Beam', 'Blizzard', 'Frost Breath', 'Avalanche'],
        'fighting': ['Karate Chop', 'Low Kick', 'Cross Chop', 'Close Combat'],
        'poison': ['Poison Sting', 'Sludge Bomb', 'Toxic', 'Venoshock'],
        'ground': ['Earthquake', 'Dig', 'Earth Power', 'Mud Bomb'],
        'flying': ['Gust', 'Aerial Ace', 'Air Slash', 'Hurricane'],
        'psychic': ['Confusion', 'Psychic', 'Psybeam', 'Psyshock'],
        'bug': ['Bug Bite', 'X-Scissor', 'Megahorn', 'Bug Buzz'],
        'rock': ['Rock Throw', 'Rock Slide', 'Stone Edge', 'Rock Wrecker'],
        'ghost': ['Shadow Ball', 'Shadow Punch', 'Hex', 'Phantom Force'],
        'dragon': ['Dragon Rage', 'Dragon Claw', 'Draco Meteor', 'Outrage'],
        'dark': ['Bite', 'Crunch', 'Dark Pulse', 'Night Slash'],
        'steel': ['Metal Claw', 'Iron Tail', 'Flash Cannon', 'Meteor Mash'],
        'fairy': ['Fairy Wind', 'Moonblast', 'Dazzling Gleam', 'Play Rough']
    }

    # Default moves for custom Pokemon or unknown types
    default_moves = ['Tackle', 'Quick Attack', 'Swift', 'Hyper Beam']

    # Determine challenger Pokemon type and moves
    if challenger_pokemon.is_custom:
        challenger_type = challenger_pokemon.type.lower()
    else:
        challenger_type = challenger_pokemon.species.types[0].lower() if challenger_pokemon.species.types else 'normal'

    challenger_moves = moves_by_type.get(challenger_type, default_moves)

    # Randomly assign a type to AI Pokemon for better battle narration
    ai_pokemon_type = random.choice(list(moves_by_type.keys()))
    ai_moves = moves_by_type.get(ai_pokemon_type, default_moves)

    # Determine Pokemon stats - this will influence battle outcome
    challenger_level = challenger_pokemon.level
    ai_level = challenger_level + random.randint(-3, 3)  # AI level is similar but varied
    ai_level = max(1, min(ai_level, 100))  # Keep level between 1 and 100

    # Base the battle outcome partly on Pokemon levels
    # Let's make it more realistic - stronger Pokemon have better chances but not guaranteed wins
    challenger_strength = challenger_level + random.randint(1, 10)
    ai_strength = ai_level + random.randint(1, 10)

    # Create battle turns
    turns = []
    challenger_hp = 100
    ai_hp = 100
    max_turns = random.randint(4, 7)  # Random number of turns for variety

    for turn in range(1, max_turns + 1):
        # Challenger's turn
        challenger_move = random.choice(challenger_moves)
        damage = random.randint(5, 20)
        if random.random() < 0.1:  # 10% chance of critical hit
            damage *= 2
            turns.append({
                "turn": turn * 2 - 1,
                "action": f"{challenger_pokemon.display_name} used {challenger_move} and scored a CRITICAL HIT dealing {damage} damage to {ai_pokemon_name}!"
            })
        else:
            turns.append({
                "turn": turn * 2 - 1,
                "action": f"{challenger_pokemon.display_name} used {challenger_move} and dealt {damage} damage to {ai_pokemon_name}!"
            })

        ai_hp -= damage
        ai_hp = max(0, ai_hp)  # Ensure HP doesn't go below 0

        # Check if battle ended
        if ai_hp == 0:
            turns.append({
                "turn": turn * 2,
                "action": f"{ai_pokemon_name} fainted!"
            })
            break

        # AI's turn
        ai_move = random.choice(ai_moves)
        # Make AI damage slightly more varied for more realistic battles
        damage = random.randint(5, 20)
        if random.random() < 0.1:  # 10% chance of critical hit
            damage *= 2
            turns.append({
                "turn": turn * 2,
                "action": f"{ai_pokemon_name} used {ai_move} and scored a CRITICAL HIT dealing {damage} damage to {challenger_pokemon.display_name}!"
            })
        else:
            turns.append({
                "turn": turn * 2,
                "action": f"{ai_pokemon_name} used {ai_move} and dealt {damage} damage to {challenger_pokemon.display_name}!"
            })

        challenger_hp -= damage
        challenger_hp = max(0, challenger_hp)  # Ensure HP doesn't go below 0

        # Check if battle ended
        if challenger_hp == 0:
            turns.append({
                "turn": turn * 2 + 1,
                "action": f"{challenger_pokemon.display_name} fainted!"
            })
            break

    # Determine winner based on remaining HP or Pokemon strength if turn limit reached
    if challenger_hp == 0:
        winner = "AI"
        summary = f"After an intense battle, {ai_pokemon_name} defeated {challenger_pokemon.display_name}!"
    elif ai_hp == 0:
        winner = "Challenger"
        summary = f"After an intense battle, {challenger_pokemon.display_name} defeated {ai_pokemon_name}!"
    else:
        # If turn limit reached, decide winner based on remaining HP percentage
        if challenger_hp > ai_hp:
            winner = "Challenger"
            summary = f"Time ran out! {challenger_pokemon.display_name} won with more health remaining ({challenger_hp}% vs {ai_hp}%)!"
        elif ai_hp > challenger_hp:
            winner = "AI"
            summary = f"Time ran out! {ai_pokemon_name} won with more health remaining ({ai_hp}% vs {challenger_hp}%)!"
        else:
            # True draw
            winner = "Draw"
            summary = f"The battle ended in a draw with both Pokemon at {challenger_hp}% health!"

    # Update battle Pokemon HP percentages for UI display
    challenger_hp_percent = challenger_hp
    ai_hp_percent = ai_hp

    return {
        "turns": turns,
        "winner": winner,
        "summary": summary,
        "challenger_hp": challenger_hp_percent,
        "ai_hp": ai_hp_percent,
        "ai_pokemon_name": ai_pokemon_name,
        "ai_pokemon_type": ai_pokemon_type
    }