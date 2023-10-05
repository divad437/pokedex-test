import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from pokemon.models import PokemonObject


class Command(BaseCommand):
    """
    Create PokedexCreature instances from CSV file
    """

    help = "Import pokemon CSV file and create PokemonObject instances"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file_path",
            type=str,
            nargs="?",
            default=os.path.join(settings.BASE_DIR, "liste_objets_pokemon.csv"),
        )

    def handle(self, *args, **options):
        csv_file_path = options.get("csv_file_path", None)
        if csv_file_path and csv_file_path.endswith(".csv"):
            with open(csv_file_path, newline="") as csvfile:
                reader = csv.reader(csvfile)
                # skip the headers:
                next(reader, None)

                creatures = [
                    PokemonObject(
                        name=row[0],
                        image_url=row[1],
                        description=row[2],
                    )
                    for row in reader
                ]

                PokemonObject.objects.bulk_create(
                    creatures,
                    batch_size=100,
                    # ignore_conflicts=True,
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Nb of pokemon objects imported to the database: "
                        f"{len(creatures)}."
                    )
                )
        else:
            self.stderr.write(self.style.ERROR("This is not a CSV file."))
