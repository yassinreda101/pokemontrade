# battles/models.py

from django.db import models
from accounts.models import Trainer
from pokemons.models import Pokemon
from django.utils import timezone
from django.conf import settings
import random
import json

from pokemon_trading_app.observers import Subject

class Battle(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    challenger = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='battles_as_challenger')
    opponent = models.ForeignKey(Trainer, null=True, blank=True, on_delete=models.CASCADE, related_name='battles_as_opponent')
    winner = models.ForeignKey(Trainer, null=True, blank=True, on_delete=models.SET_NULL, related_name='battles_won')
    battle_log = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_ai_opponent = models.BooleanField(default=False)  # << ADD THIS LINE
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Battle #{self.id}: {self.challenger} vs {self.opponent}"

    def respond_to_challenge(self, opponent_pokemon):
        """
        Opponent responds to a battle challenge.
        """
        if self.status != 'pending':
            return False, "This battle challenge is no longer available"

        if self.opponent != opponent_pokemon.trainer:
            return False, "You cannot respond to this challenge"

        # Add opponent's Pokemon to the battle
        BattlePokemon.objects.create(
            battle=self,
            pokemon=opponent_pokemon,
            trainer=self.opponent,
            current_hp=opponent_pokemon.stats.get('hp', 100) if not opponent_pokemon.is_custom else 100
        )

        # Update battle status
        self.status = 'in_progress'
        self.save()

        # Simulate the battle
        self.simulate_player_battle()

        return True, "You have accepted the challenge! The battle has been simulated."

    def simulate_player_battle(self):
        """
        Simulate a battle between the two players.
        """
        challenger_battle_pokemon = BattlePokemon.objects.filter(battle=self, trainer=self.challenger).first()
        opponent_battle_pokemon = BattlePokemon.objects.filter(battle=self, trainer=self.opponent).first()

        if not challenger_battle_pokemon or not opponent_battle_pokemon:
            return False, "Both trainers must select Pokemon for the battle"

        challenger_pokemon = challenger_battle_pokemon.pokemon
        opponent_pokemon = opponent_battle_pokemon.pokemon

        challenger_strength = challenger_pokemon.level + random.randint(1, 10)
        opponent_strength = opponent_pokemon.level + random.randint(1, 10)

        # Battle Simulation
        turns = []
        challenger_hp = 100
        opponent_hp = 100
        max_turns = random.randint(4, 7)

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
            'fairy': ['Fairy Wind', 'Moonblast', 'Dazzling Gleam', 'Play Rough'],
        }
        default_moves = ['Tackle', 'Quick Attack', 'Swift', 'Hyper Beam']

        challenger_moves = moves_by_type.get(
            (challenger_pokemon.type.lower() if challenger_pokemon.is_custom else (challenger_pokemon.species.types[0].lower() if challenger_pokemon.species.types else 'normal')),
            default_moves
        )

        opponent_moves = moves_by_type.get(
            (opponent_pokemon.type.lower() if opponent_pokemon.is_custom else (opponent_pokemon.species.types[0].lower() if opponent_pokemon.species.types else 'normal')),
            default_moves
        )

        for turn in range(1, max_turns + 1):
            challenger_move = random.choice(challenger_moves)
            damage = random.randint(5, 20)
            if random.random() < 0.1:
                damage *= 2
                turns.append({
                    "turn": turn * 2 - 1,
                    "action": f"{challenger_pokemon.display_name} used {challenger_move} and scored a CRITICAL HIT dealing {damage} damage to {opponent_pokemon.display_name}!"
                })
            else:
                turns.append({
                    "turn": turn * 2 - 1,
                    "action": f"{challenger_pokemon.display_name} used {challenger_move} and dealt {damage} damage to {opponent_pokemon.display_name}."
                })

            opponent_hp = max(0, opponent_hp - damage)
            if opponent_hp == 0:
                turns.append({
                    "turn": turn * 2,
                    "action": f"{opponent_pokemon.display_name} fainted!"
                })
                break

            opponent_move = random.choice(opponent_moves)
            damage = random.randint(5, 20)
            if random.random() < 0.1:
                damage *= 2
                turns.append({
                    "turn": turn * 2,
                    "action": f"{opponent_pokemon.display_name} used {opponent_move} and scored a CRITICAL HIT dealing {damage} damage to {challenger_pokemon.display_name}!"
                })
            else:
                turns.append({
                    "turn": turn * 2,
                    "action": f"{opponent_pokemon.display_name} used {opponent_move} and dealt {damage} damage to {challenger_pokemon.display_name}."
                })

            challenger_hp = max(0, challenger_hp - damage)
            if challenger_hp == 0:
                turns.append({
                    "turn": turn * 2 + 1,
                    "action": f"{challenger_pokemon.display_name} fainted!"
                })
                break

        challenger_battle_pokemon.current_hp = challenger_hp
        opponent_battle_pokemon.current_hp = opponent_hp
        challenger_battle_pokemon.save()
        opponent_battle_pokemon.save()

        if challenger_hp == 0:
            winner = self.opponent
            summary = f"{opponent_pokemon.display_name} defeated {challenger_pokemon.display_name}!"
        elif opponent_hp == 0:
            winner = self.challenger
            summary = f"{challenger_pokemon.display_name} defeated {opponent_pokemon.display_name}!"
        else:
            if challenger_hp > opponent_hp:
                winner = self.challenger
                summary = f"Time ran out! {challenger_pokemon.display_name} won with {challenger_hp}% HP remaining."
            elif opponent_hp > challenger_hp:
                winner = self.opponent
                summary = f"Time ran out! {opponent_pokemon.display_name} won with {opponent_hp}% HP remaining."
            else:
                winner = None
                summary = "The battle ended in a draw!"

        self.battle_log = {
            "turns": turns,
            "summary": summary,
            "challenger_hp": challenger_hp,
            "opponent_hp": opponent_hp
        }
        self.status = 'completed'
        self.winner = winner
        self.completed_at = timezone.now()
        self.save()

        if winner:
            winner.increase_xp(100)
            if winner == self.challenger:
                challenger_pokemon.experience += 50
                challenger_pokemon.save()
            else:
                opponent_pokemon.experience += 50
                opponent_pokemon.save()

        try:
            from achievements.services import check_achievements
            if self.challenger:
                check_achievements(self.challenger)
            if self.opponent:
                check_achievements(self.opponent)
        except ImportError:
            pass

        return True

class BattlePokemon(models.Model):
    """
    Pokemon participating in a battle.
    """
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE, related_name='battle_pokemons')
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    current_hp = models.IntegerField()

    def __str__(self):
        return f"{self.pokemon.display_name} in Battle #{self.battle.id}"

    def save(self, *args, **kwargs):
        if not self.pk and self.current_hp is None:
            self.current_hp = self.pokemon.stats.get('hp', 50)
        super().save(*args, **kwargs)
