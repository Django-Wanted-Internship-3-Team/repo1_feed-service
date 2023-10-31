import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class SignupViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.confirmed_user = User.objects.create_user(
            email="testuser1@example.com", username="testusername1", password="testpassword", is_confirmed=True
        )
        cls.not_confirmed_user = User.objects.create_user(
            email="testuser2@example.com", username="testusername2", password="testpassword", is_confirmed=False
        )

    def test_post_login_success(self):
        response = self.client.post(
            path=reverse("login"),
            data=json.dumps(
                {
                    "username": "testusername1",
                    "password": "testpassword",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.confirmed_user.is_active, True)

    def test_post_login_fail_user_not_found(self):
        response = self.client.post(
            path=reverse("login"),
            data=json.dumps(
                {
                    "username": "testusername3",
                    "password": "testpassword",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_login_fail_invalid_password(self):
        response = self.client.post(
            path=reverse("login"),
            data=json.dumps(
                {
                    "username": "testusername1",
                    "password": "testpassword2",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_login_fail_not_confirmed_user(self):
        response = self.client.post(
            path=reverse("login"),
            data=json.dumps(
                {
                    "username": "testusername2",
                    "password": "testpassword",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
