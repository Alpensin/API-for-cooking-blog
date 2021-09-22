from rest_framework import viewsets

from api.filters import RecipeFilter
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import RecipeSerializer
from recipes.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_class = RecipeFilter
