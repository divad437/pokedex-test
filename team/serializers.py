from rest_framework import serializers

from pokemon.serializers import PokemonSerializer
from .models import PokemonTeam, Pokemon


class PokemonTeamSerializer(serializers.ModelSerializer):
    # all informations about the pokemons in the team
    pokemons = serializers.SerializerMethodField()

    def get_pokemons(self, obj):
        pokemons = Pokemon.objects.filter(teams=obj)
        return PokemonSerializer(pokemons, many=True).data

    class Meta:
        model = PokemonTeam
        fields = ('id', 'name', 'pokemons')
        read_only_fields = ('id', 'trainer')


class PokemonTeamAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = ('id', 'team')
