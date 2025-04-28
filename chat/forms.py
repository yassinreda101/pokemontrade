# chat/forms.py

from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import ChatRoom

class RoomForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = ChatRoom
        fields = ['name', 'participants']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Exclude current user and admin users from participants
            self.fields['participants'].queryset = get_user_model().objects.exclude(
                Q(id=user.id) | Q(is_staff=True) | Q(is_superuser=True)
            )