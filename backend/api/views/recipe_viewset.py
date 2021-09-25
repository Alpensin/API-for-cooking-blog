from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (
    BriefRecipeSerializer,
    RecipeFavoritesSerializer,
    RecipeSerializer,
)
from recipes.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_class = RecipeFilter

    @action(detail=True, permission_classes=[IsAuthenticated], methods=["get"])
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        data = {
            "user": user.id,
            "recipe": recipe.id,
        }
        serializer = RecipeFavoritesSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        recipe.in_favorites = recipe.in_favorites.exclude(pk=user.pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
