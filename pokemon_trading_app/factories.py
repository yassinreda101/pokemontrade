# pokemon_trading_app/factories.py

from abc import ABC, abstractmethod
import random

class PokemonFactory(ABC):
    """
    Abstract Factory for creating Pokemon objects
    """
    @abstractmethod
    def create_pokemon(self, trainer):
        pass

class StarterPokemonFactory(PokemonFactory):
    """
    Factory for creating starter Pokemon
    """
    def create_pokemon(self, trainer):
        # List of starter Pokemon IDs (based on PokeAPI)
        starter_ids = [1, 4, 7, 25, 133, 152, 155, 158, 252, 255, 258, 387, 390, 393]

        # Randomly select 3 starter Pokemon
        selected_ids = random.sample(starter_ids, 3)
        created_pokemon = []

        from pokemons.models import Pokemon

        # Add a common, uncommon, and rare Pokemon to ensure variety
        rarities = ['common', 'uncommon', 'rare']

        for i, pokemon_id in enumerate(selected_ids):
            # Assign different rarities to starter Pokémon
            rarity = rarities[i] if i < len(rarities) else random.choice(rarities)

            # Create Pokemon object with assigned rarity
            pokemon = Pokemon.create_from_api(pokemon_id=pokemon_id, trainer=trainer, rarity=rarity)

            if pokemon:
                created_pokemon.append(pokemon)

        return created_pokemon


class RandomPokemonFactory(PokemonFactory):
    """
    Factory for creating random Pokemon
    """
    def create_pokemon(self, trainer, count=1, rarity_weights=None):
        if rarity_weights is None:
            rarity_weights = {'common': 70, 'uncommon': 20, 'rare': 9, 'legendary': 1}

        # Get total number of Pokemon from PokeAPI
        # For this example, we'll use 898 (Gen 8)
        max_pokemon_id = 898

        created_pokemon = []
        from pokemons.models import Pokemon
        for _ in range(count):
            # Randomly select Pokemon ID
            pokemon_id = random.randint(1, max_pokemon_id)

            # Determine rarity based on weights
            rarity = random.choices(
                list(rarity_weights.keys()),
                weights=list(rarity_weights.values())
            )[0]

            # Create Pokemon object
            pokemon = Pokemon.create_from_api(pokemon_id=pokemon_id, trainer=trainer, rarity=rarity)
            if pokemon:
                created_pokemon.append(pokemon)

        return created_pokemon

class CustomPokemonFactory(PokemonFactory):
    """
    Factory for creating custom Pokemon
    """
    def create_pokemon(self, trainer, name=None, type=None):
        from pokemons.services import generate_pokemon_image
        from pokemons.models import Pokemon

        # Generate a custom Pokemon image (placeholder for now)
        image_url = generate_pokemon_image(name, type)

        # Create Pokemon object with custom image
        pokemon = Pokemon.objects.create(
            name=name,
            type=type,
            trainer=trainer,
            rarity='custom',
            image_url=image_url,
            is_custom=True
        )

        return pokemon