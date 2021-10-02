from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Follow, Recipe

from .recipe_serializer import BriefRecipeSerializer
from .user_serializer import CustomUserSerializer

User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for Follow model"""

    queryset = User.objects.all()
    user = serializers.PrimaryKeyRelatedField(queryset=queryset)
    author = serializers.PrimaryKeyRelatedField(queryset=queryset)

    class Meta:
        model = Follow
        fields = ("user", "author")

    def validate(self, data):
        request = self.context["request"]
        author = data["author"]

        if request.method == "GET":
            if request.user == author:
                raise serializers.ValidationError(
                    "Нельзя подписаться на самого себя"
                )
            if Follow.objects.filter(
                user=request.user, author=author
            ).exists():
                raise serializers.ValidationError(
                    "Вы уже подписаны на этого автора"
                )
        return data


class FollowerSerializer(CustomUserSerializer):
    """Serializer for User model to serialize following information"""

    email = serializers.ReadOnlyField(source="author.email")
    id = serializers.ReadOnlyField(source="author.id")
    username = serializers.ReadOnlyField(source="author.username")
    first_name = serializers.ReadOnlyField(source="author.first_name")
    last_name = serializers.ReadOnlyField(source="author.last_name")
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=obj.user, author=obj.author).exists()

    def get_recipes(self, obj):
        request = self.context.get("request")
        limit = request.GET.get("recipes_limit")
        queryset = Recipe.objects.filter(author=obj.author)
        if limit is not None:
            queryset = Recipe.objects.filter(author=obj.author)[: int(limit)]

        return BriefRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
