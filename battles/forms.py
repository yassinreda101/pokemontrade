# battles/forms.py

from django import forms
from django.db.models import Q
from .models import Battle
from pokemons.models import Pokemon
from accounts.models import Trainer

class BattleAIForm(forms.Form):
    pokemon = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Only show Pokemon owned by this user
            self.fields['pokemon'].queryset = Pokemon.objects.filter(trainer=user)

class BattlePlayerForm(forms.Form):
    opponent = forms.ModelChoiceField(
        queryset=None,
        label="Opponent",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    pokemon = forms.ModelChoiceField(
        queryset=None,
        label="Your Pokemon",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Exclude current user and admin users from opponents
            self.fields['opponent'].queryset = Trainer.objects.exclude(
                Q(id=user.id) | Q(is_staff=True) | Q(is_superuser=True)
            )

            # Only show Pokemon owned by this user
            self.fields['pokemon'].queryset = Pokemon.objects.filter(trainer=user)