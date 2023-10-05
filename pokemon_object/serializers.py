from rest_framework import serializers

from .models import PokemonObject


class PokemonObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonObject
        fields = (
            'id',
            'name',
            'image_url',
            'description',
        )
        read_only_fields = ('id',)
