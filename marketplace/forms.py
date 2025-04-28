# marketplace/forms.py

from django import forms
from .models import MarketplaceListing
from pokemons.models import Pokemon

class ListingForm(forms.ModelForm):
    class Meta:
        model = MarketplaceListing
        fields = ['pokemon', 'price', 'description']
        widgets = {
            'pokemon': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Only show Pokemon owned by this user that are not already listed
            listed_pokemon_ids = MarketplaceListing.objects.filter(
                seller=user, status='active'
            ).values_list('pokemon_id', flat=True)

            self.fields['pokemon'].queryset = Pokemon.objects.filter(
                trainer=user
            ).exclude(
                id__in=listed_pokemon_ids
            )

class PurchaseForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label='I confirm this purchase',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )