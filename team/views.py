from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view

from pokemon.models import Pokemon
from .filters import PokemonTeamFilter
from .models import PokemonTeam, PokemonTeamPokemon
from .serializers import PokemonTeamSerializer


@extend_schema_view(
    create=extend_schema(
        description="API endpoint to create a pokemon team"
    ),
    list=extend_schema(
        description="API endpoint to get a list of pokemon teams, with filtering options"
    ),
    retrieve=extend_schema(
        description="API endpoint to retrieve a specific pokemon team, which gives on him detailed informations"
    ),
    update=extend_schema(description="API endpoint to modify a specific pokemon team"),
    partial_update=extend_schema(
        description="API endpoint to partially modify a specific pokemon team"
    ),
    destroy=extend_schema(
        description="API endpoint to delete a specific pokemon team. It's horrible"
    ),
    assign_pokemon=extend_schema(
        description="API endpoint to assign a pokemon to a team."
                    " Need a pokemon_id in the request body and "
                    "a team_id in the url and name of the pokemon team"
    ),
    remove_pokemon=extend_schema(
        description="API endpoint to remove a pokemon from a team."
                    "Need a pokemon_id in the request body and"
                    "a team_id in the url and name of the pokemon team"
    ),
)
class PokemonTeamViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PokemonTeamSerializer
    # filter_backends = [DjangoFilterBackend]

    # filterset_class = PokemonTeamFilter

    def get_queryset(self):
        return PokemonTeam.objects.filter(trainer=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(trainer=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(trainer=self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'team_ids': [team.id for team in queryset]})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.trainer == self.request.user:
            return super().update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.trainer == self.request.user:
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.trainer == self.request.user:
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'], url_path='assign-pokemon')
    def assign_pokemon(self, request, pk=None):
        team = self.get_object()
        pokemon_assign = ""
        pokemon_id = request.data.get('pokemon_id')
        if team.trainer == self.request.user and pokemon_id:
            try:
                pokemon = Pokemon.objects.get(id=pokemon_id, trainer=self.request.user)
            except Pokemon.DoesNotExist:
                return Response({'message': 'Pokemon not found.'}, status=status.HTTP_404_NOT_FOUND)
            pokemon_assign = PokemonTeamPokemon.objects.filter(pokemon=pokemon).first()
            if pokemon_assign is not None:
                return Response({'message': 'Pokemon is already assigned to a team.'},
                                status=status.HTTP_400_BAD_REQUEST)
            team.pokemons.add(pokemon)
            return Response({'message': 'Pokemon assigned successfully.'})
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    # def perform_create(self, serializer):
    #     serializer.save(trainer=self.request.user)

    @action(detail=True, methods=['post'], url_path='remove-pokemon')
    def remove_pokemon(self, request, pk=None):
        team = self.get_object()
        pokemon_id = request.data.get('pokemon_id')
        if team.trainer == self.request.user and pokemon_id:
            team.pokemons.remove(pokemon_id)
            return Response({'message': 'Pokemon removed successfully.'})
