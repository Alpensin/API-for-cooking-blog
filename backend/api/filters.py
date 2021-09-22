import django_filters as filters
from django.contrib.auth import get_user_model

from recipes.models import Ingredient, Recipe

User = get_user_model()


class IngredientNameFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="istartswith")

    class Meta:
        model = Ingredient
        fields = ("name", "measurement_unit")


class RecipeFilter(filters.FilterSet):
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.AllValuesMultipleFilter(field_name="tags__slug")

    class Meta:
        model = Recipe
        fields = ["author", "tags"]
