from django.contrib import admin
from .models import PokemonTeam, PokemonTeamPokemon


class PokemonTeamPokemonInline(admin.TabularInline):
    model = PokemonTeamPokemon
    extra = 1


class PokemonTeamAdmin(admin.ModelAdmin):
    inlines = (PokemonTeamPokemonInline,)
    list_display = ('name', 'trainer')
    list_filter = ('trainer',)
    search_fields = ('name', 'trainer__username')


admin.site.register(PokemonTeam, PokemonTeamAdmin)
admin.site.register(PokemonTeamPokemon)
