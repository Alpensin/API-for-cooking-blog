import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "loads ingredients from ingredients.csv"

    def handle(self, *args, **options):
        file_path = settings.BASE_DIR / "data" / "ingredients.csv"
        with open(file_path, "r", encoding="utf-8") as f:
            ingredients_and_units = csv.reader(f)
            bulk_create_ingredients = (
                Ingredient(name=ingredient[0], measurement_unit=ingredient[1])
                for ingredient in ingredients_and_units
            )
            Ingredient.objects.bulk_create(bulk_create_ingredients)
