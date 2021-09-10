import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Unit


class Command(BaseCommand):
    help = "loads ingredients from ingredients.csv"

    def handle(self, *args, **options):
        file_path = settings.BASE_DIR / "recipes/data/ingredients.csv"
        with open(file_path, "r") as f:
            ingredients_and_units = csv.reader(f)
            bulk_create_ingredients = list()
            bulk_create_ingredients = (
                Ingredient(*ingredient) for ingredient in ingredients_and_units
            )
            # for ingredient in ingredients_and_units:
            #     ingredient_title, unit_name = ingredient
            #     ingredient = Ingredient(title=ingredient_title, unit=unit_name)
            #     bulk_create_ingredients.append(ingredient)
            Ingredient.objects.bulk_create(bulk_create_ingredients)
