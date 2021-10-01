from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.custom_fields import CustomDecimalField
from api.validators import (
    IngredientsAmountIsPovitiveValidator,
    UniqueIngredientsGivenValidator,
)
from recipes.models import Favorite, IngredientForRecipe, Purchase, Recipe, Tag

from .user_serializer import CustomUserSerializer

User = get_user_model()


class BriefRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = IngredientForRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    author = CustomUserSerializer(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientForRecipeSerializer(
        source="ingredientsforrecipe",
        many=True,
    )
    image = Base64ImageField()
    cooking_time = CustomDecimalField(max_digits=4, decimal_places=1)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        validators = {
            "ingredients": (
                UniqueIngredientsGivenValidator,
                IngredientsAmountIsPovitiveValidator,
            ),
        }

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            recipe=obj,
            user=request.user,
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False
        return Purchase.objects.filter(user=request.user, recipe=obj).exists()

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        tags = self.initial_data.get("tags")

        for tag_id in tags:
            recipe.tags.add(get_object_or_404(Tag, pk=tag_id))

        for ingredient in ingredients:
            id_ = ingredient.get("id")
            amount = ingredient.get("amount")
            IngredientForRecipe.objects.create(
                recipe=recipe, ingredient_id=id_, amount=amount
            )

        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        tags = self.initial_data.get("tags")

        for tag_id in tags:
            instance.tags.add(get_object_or_404(Tag, pk=tag_id))

        IngredientForRecipe.objects.filter(recipe=instance).delete()
        for ingredient in validated_data.get("ingredients"):
            ingredients_amounts = IngredientForRecipe.objects.create(
                recipe=instance,
                ingredient_id=ingredient.get("id"),
                amount=ingredient.get("amount"),
            )
            ingredients_amounts.save()

        if validated_data.get("image") is not None:
            instance.image = validated_data.get("image")
        instance.name = validated_data.get("name")
        instance.text = validated_data.get("text")
        instance.cooking_time = validated_data.get("cooking_time")
        instance.save()

        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = (
            "user",
            "recipe",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=[
                    "user",
                    "recipe",
                ],
                message="Рецепт уже в избранном.",
            )
        ]

    def to_representation(self, instance):
        request = self.context.get("request")
        context = {"request": request}
        return BriefRecipeSerializer(instance.recipe, context=context).data


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = (
            "user",
            "recipe",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Purchase.objects.all(),
                fields=[
                    "user",
                    "recipe",
                ],
                message="Рецепт уже в списке покупок.",
            )
        ]

    def to_representation(self, instance):
        request = self.context.get("request")
        context = {"request": request}
        return BriefRecipeSerializer(
            instance.recipe,
            context=context,
        ).data
