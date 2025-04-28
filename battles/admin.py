# battles/admin.py

from django.contrib import admin
from .models import Battle, BattlePokemon

class BattlePokemonInline(admin.TabularInline):
    model = BattlePokemon
    extra = 1

class BattleAdmin(admin.ModelAdmin):
    list_display = ('id', 'challenger', 'opponent', 'status', 'is_ai_opponent', 'created_at')
    list_filter = ('status', 'is_ai_opponent')
    search_fields = ('challenger__username', 'opponent__username')
    inlines = [BattlePokemonInline]

admin.site.register(Battle, BattleAdmin)