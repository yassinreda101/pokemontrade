# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Trainer(AbstractUser):
    """
    Custom user model for Pokemon trainers
    """
    email = models.EmailField(_('email address'), unique=True)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        default='defaults/default_profile.png',
        null=True,
        blank=True
    )
    currency = models.IntegerField(default=1000)  # In-game currency
    experience_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    # Custom fields for trainers
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    favorite_type = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def increase_xp(self, amount):
        self.experience_points += amount
        # Check if trainer leveled up
        new_level = (self.experience_points // 1000) + 1
        if new_level > self.level:
            self.level = new_level
        self.save()