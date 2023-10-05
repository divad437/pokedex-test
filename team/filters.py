# pokemon/filters.py
import django_filters
from .models import Pokemon


class PokemonTeamFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')  # Filtre de recherche partielle

    class Meta:
        model = Pokemon
        fields = ['name']  # Les champs que vous souhaitez filtrer
