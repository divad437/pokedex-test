# pokemon/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PokemonTeamViewSet

app_name = 'team'

router = DefaultRouter()
router.register('', PokemonTeamViewSet, basename='team')

urlpatterns = [
    path('', include(router.urls)),
]
