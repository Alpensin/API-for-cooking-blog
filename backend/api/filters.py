import django_filters as filters

from recipes.models import Ingredient


class IngredientNameFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="istartswith")

    class Meta:
        model = Ingredient
        fields = ("name", "measurement_unit")
