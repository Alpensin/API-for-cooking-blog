from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import FollowerSerializer, FollowSerializer
from recipes.models import Follow

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    @action(detail=True, permission_classes=[IsAuthenticated], methods=["get"])
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        data = {
            "user": user.id,
            "author": author.id,
        }
        serializer = FollowSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        subscribe = get_object_or_404(Follow, user=user, author=author)
        subscribe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, permission_classes=[IsAuthenticated], methods=["get"]
    )
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowerSerializer(
            pages, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)
