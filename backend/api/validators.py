from decimal import Decimal

from rest_framework.serializers import ValidationError


class UniqueIngredientsGivenValidator:
    message = "Ингредиент указан в рецепте более одного раза"

    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        ingredients = self.initial_data.get("ingredients")
        if len(ingredients) != len(set(ingredients)):
            raise ValidationError(self.message, code="unique")


class IngredientsAmountIsPovitiveValidator:
    message = "Количество ингредиентов меньше или равно нулю"

    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        ingredients = self.initial_data.get("ingredients")
        if any(
            int(ingredient.get("amount", -1)) for ingredient in ingredients
        ):
            raise ValidationError(self.message)


class CookingTimeIsPovitiveValidator:
    message = "Задано отрицательное время приготовления"

    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        cooking_time = Decimal(self.initial_data.get("cooking_time"))
        if cooking_time <= 0:
            raise ValidationError(self.message)
