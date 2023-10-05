from django.db.models import Q
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import PokemonObject
from .serializers import PokemonObjectSerializer
from .filters import PokemonObjectFilter


class PokemonObjectViewSet(ReadOnlyModelViewSet):
    queryset = PokemonObject.objects.all()
    serializer_class = PokemonObjectSerializer
    filterset_class = PokemonObjectFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        name_query = self.request.query_params.get('name', None)
        if name_query:
            queryset = queryset.filter(Q(name__icontains=name_query))
        return queryset
