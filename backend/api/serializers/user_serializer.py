from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, validators

from recipes.models import Follow

User = get_user_model()


class UserRegistrationSerializer(UserCreateSerializer):
    """To register new user"""

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("email", "username", "first_name", "last_name", "password")


class CustomUserSerializer(UserSerializer):
    """To provide User info"""

    email = serializers.EmailField(
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, instance):
        request = self.context["request"]
        if request.user.is_anonymous or request.user == instance:
            return False
        return Follow.objects.filter(
            user=request.user, author=instance
        ).exists()
