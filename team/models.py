from django.db import models
from django.contrib.auth.models import User

from pokemon.models import Pokemon


class PokemonTeam(models.Model):
    pokemons = models.ManyToManyField(
        Pokemon,
        related_name="teams",
        through="PokemonTeamPokemon",
    )
    trainer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{}'s team {}".format(self.trainer.username, self.name)


class PokemonTeamPokemon(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.DO_NOTHING
    )
    pokemon_team = models.ForeignKey(
        PokemonTeam,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ["pokemon_team", "pokemon"]
