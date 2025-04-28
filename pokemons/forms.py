# pokemons/forms.py

from django import forms
from .models import Pokemon

class PokemonSearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        label='Search',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    type_filter = forms.ChoiceField(
        choices=[('', 'All Types')],
        required=False,
        label='Type',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    rarity_filter = forms.ChoiceField(
        choices=[('', 'All Rarities')] + Pokemon.RARITY_CHOICES,
        required=False,
        label='Rarity',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get all unique Pokemon types
        all_types = [
            'normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting',
            'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost',
            'dragon', 'dark', 'steel', 'fairy'
        ]
        self.fields['type_filter'].choices = [('', 'All Types')] + [(t, t.capitalize()) for t in all_types]

class CustomPokemonForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Pokemon Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    type = forms.ChoiceField(
        label='Pokemon Type',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get all unique Pokemon types
        all_types = [
            'normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting',
            'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost',
            'dragon', 'dark', 'steel', 'fairy'
        ]
        self.fields['type'].choices = [(t, t.capitalize()) for t in all_types]