# pokemons/admin.py

from django.contrib import admin
from .models import PokemonSpecies, Pokemon

class PokemonSpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_id')
    search_fields = ('name',)

class PokemonAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'trainer', 'rarity', 'level', 'is_custom')
    list_filter = ('rarity', 'is_custom')
    search_fields = ('nickname', 'name')

admin.site.register(PokemonSpecies, PokemonSpeciesAdmin)
admin.site.register(Pokemon, PokemonAdmin)