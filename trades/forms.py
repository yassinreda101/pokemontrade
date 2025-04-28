# trades/forms.py

from django import forms
from django.db.models import Q
from .models import Trade
from pokemons.models import Pokemon

class TradeForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )

    class Meta:
        model = Trade
        fields = ['recipient', 'message']
        widgets = {
            'recipient': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Exclude current user and admin users from recipients
            self.fields['recipient'].queryset = self.fields['recipient'].queryset.exclude(
                Q(id=user.id) | Q(is_staff=True) | Q(is_superuser=True)
            )

class TradeItemForm(forms.Form):
    pokemon = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        trainer = kwargs.pop('trainer', None)
        super().__init__(*args, **kwargs)

        if trainer:
            # Only show Pokemon owned by this trainer
            self.fields['pokemon'].queryset = Pokemon.objects.filter(trainer=trainer)

class TradeRespondForm(forms.Form):
    action = forms.ChoiceField(
        choices=[('accept', 'Accept Trade'), ('reject', 'Reject Trade')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )