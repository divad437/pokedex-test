from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PokemonObjectViewSet

app_name = "pokemon_objects"

router = DefaultRouter()
router.register('', PokemonObjectViewSet, basename='pokemonobject')


urlpatterns = [
    path("", include(router.urls)),
]
