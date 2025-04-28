# pokemons/models.py

from django.db import models
import requests
import random
import json
from django.conf import settings
from accounts.models import Trainer

class PokemonSpecies(models.Model):
    """
    Model to store Pokemon species data from PokeAPI
    """
    api_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    types = models.JSONField()  # Store as JSON array
    height = models.IntegerField()
    weight = models.IntegerField()
    abilities = models.JSONField()  # Store as JSON array
    base_experience = models.IntegerField()
    stats = models.JSONField()  # Store as JSON array
    image_url = models.URLField()

    def __str__(self):
        return self.name

    @classmethod
    def fetch_from_api(cls, pokemon_id):
        """
        Fetch Pokemon data from PokeAPI and store it in the database
        """
        # Check if we already have this Pokemon
        try:
            return cls.objects.get(api_id=pokemon_id)
        except cls.DoesNotExist:
            pass

        # Fetch from API
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
        if response.status_code == 200:
            data = response.json()

            # Extract types
            types = [t['type']['name'] for t in data['types']]

            # Extract abilities
            abilities = [a['ability']['name'] for a in data['abilities']]

            # Extract stats
            stats = {s['stat']['name']: s['base_stat'] for s in data['stats']}

            # Create and save the species
            species = cls(
                api_id=pokemon_id,
                name=data['name'],
                types=types,
                height=data['height'],
                weight=data['weight'],
                abilities=abilities,
                base_experience=data['base_experience'],
                stats=stats,
                image_url=data['sprites']['other']['official-artwork']['front_default']
            )
            species.save()
            return species

        # If API request fails
        return None

class Pokemon(models.Model):
    """
    Model for individual Pokemon owned by trainers
    """
    RARITY_CHOICES = [
        ('common', 'Common'),
        ('uncommon', 'Uncommon'),
        ('rare', 'Rare'),
        ('legendary', 'Legendary'),
        ('custom', 'Custom'),
    ]

    species = models.ForeignKey(PokemonSpecies, on_delete=models.CASCADE, null=True, blank=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='pokemons')
    nickname = models.CharField(max_length=100, blank=True)
    level = models.IntegerField(default=5)
    experience = models.IntegerField(default=0)
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES, default='common')
    is_favorite = models.BooleanField(default=False)
    acquired_date = models.DateTimeField(auto_now_add=True)

    # For custom Pokemon created with DALL-E
    is_custom = models.BooleanField(default=False)
    name = models.CharField(max_length=100, blank=True)  # Only for custom Pokemon
    type = models.CharField(max_length=50, blank=True)   # Only for custom Pokemon
    image_url = models.URLField(blank=True)              # Only for custom Pokemon

    def __str__(self):
        if self.is_custom:
            return self.name
        return f"{self.nickname or self.species.name}"

    @property
    def display_name(self):
        if self.is_custom:
            return self.name
        if self.nickname:
            return f"{self.nickname} ({self.species.name})"
        return self.species.name

    @property
    def image(self):
        if self.is_custom:
            return self.image_url
        return self.species.image_url

    @property
    def types(self):
        if self.is_custom:
            return [self.type]
        return self.species.types

    @property
    def stats(self):
        if self.is_custom:
            # Generate random stats for custom Pokemon
            import random
            return {
                'hp': random.randint(50, 100),
                'attack': random.randint(50, 100),
                'defense': random.randint(50, 100),
                'special-attack': random.randint(50, 100),
                'special-defense': random.randint(50, 100),
                'speed': random.randint(50, 100)
            }
        return self.species.stats

    @classmethod
    def create_from_api(cls, pokemon_id, trainer, rarity=None, nickname=''):
        """
        Create a Pokemon instance from PokeAPI data with proper rarity assignment
        """
        species = PokemonSpecies.fetch_from_api(pokemon_id)
        if species:
            # If rarity isn't specified, determine it based on the Pokemon's properties
            if rarity is None:
                # Legendary Pokemon (based on a list of known legendary Pokemon IDs)
                legendary_ids = [144, 145, 146, 150, 151, 243, 244, 245, 249, 250, 251, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 716, 717, 718, 719, 720, 721, 785, 786, 787, 788, 789, 790, 791, 792, 800, 801, 802, 807, 808, 809, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 898]

                # Rare Pokemon (starters, pseudo-legendaries, etc.)
                rare_ids = [3, 6, 9, 149, 154, 157, 160, 248, 257, 260, 282, 373, 376, 445, 448, 452, 475, 609, 612, 625, 635, 637, 652, 655, 658, 681, 687, 697, 699, 700, 701, 706, 773, 784, 812, 815, 818, 823, 835, 839, 841, 842, 862, 887]

                # Uncommon Pokemon (evolutions and less common species)
                uncommon_ids = list(range(1, 899))
                for id in legendary_ids + rare_ids + [i for i in range(1, 30)]:
                    if id in uncommon_ids:
                        uncommon_ids.remove(id)

                # Determine rarity based on ID lists and base stats
                if pokemon_id in legendary_ids:
                    rarity = 'legendary'
                elif pokemon_id in rare_ids:
                    rarity = 'rare'
                elif pokemon_id in uncommon_ids:
                    # For uncommon, use a 70/30 split to make some truly common
                    if random.random() < 0.7:
                        rarity = 'uncommon'
                    else:
                        rarity = 'common'
                else:
                    rarity = 'common'

            # Set default level based on rarity
            if rarity == 'common':
                level = random.randint(5, 20)
            elif rarity == 'uncommon':
                level = random.randint(15, 35)
            elif rarity == 'rare':
                level = random.randint(30, 50)
            elif rarity == 'legendary':
                level = random.randint(45, 70)
            else:
                level = 5

            pokemon = cls(
                species=species,
                trainer=trainer,
                nickname=nickname,
                rarity=rarity,
                level=level
            )
            pokemon.save()
            return pokemon
        return None