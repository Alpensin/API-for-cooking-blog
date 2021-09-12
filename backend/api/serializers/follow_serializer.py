from django.contrib.auth import get_user_model
from recipes.models import Follow
from rest_framework import serializers

User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()
    user = serializers.PrimaryKeyRelatedField(queryset=queryset)
    author = serializers.PrimaryKeyRelatedField(queryset=queryset)

    class Meta:
        model = Follow
        fields = ("user", "author")

    def validate(self, data):
        request = self.context["request"]
        author_id = data["author"].id

        if request.method == "GET":
            if request.user.id == author_id:
                raise serializers.ValidationError(
                    "Нельзя подписаться на самого себя"
                )
            if Follow.objects.filter(
                user=request.user, author__id=author_id
            ).exists():
                raise serializers.ValidationError(
                    "Вы уже подписаны на этого автора"
                )
        return data
