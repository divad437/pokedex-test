import django_filters
from .models import PokemonObject


class PokemonObjectFilter(django_filters.FilterSet):
    """Filters for pokemon object listing"""

    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = PokemonObject
        fields = ["name"]
