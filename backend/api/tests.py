from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

User = get_user_model()


class UserTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse("api:users-list")
        data = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "SD#SF177",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "vpupkin@yandex.ru")

    def test_user_list_authenticated(self):
        """
        Ensure we can get users list.
        """
        url = reverse("api:users-list")
        user = User.objects.create(username="olivia", email="olivia@ya.ru")
        User.objects.create(username="ash", email="ash@ya.ru")
        force_authenticate(user)
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["count"], 2)

    def test_user_list_not_authenticated(self):
        """
        Ensure we can get users list.
        """
        User.objects.create(username="olivia", email="olivia@ya.ru")
        User.objects.create(username="ash", email="ash@ya.ru")
        url = reverse("api:users-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["count"], 2)
