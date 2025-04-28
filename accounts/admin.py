# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Trainer

class TrainerAdmin(UserAdmin):
    list_display = ('username', 'email', 'level', 'currency', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'level')
    search_fields = ('username', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('Trainer Info', {'fields': ('profile_image', 'currency', 'experience_points', 'level', 'bio', 'location', 'favorite_type')}),
    )

admin.site.register(Trainer, TrainerAdmin)