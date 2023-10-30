import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class SignupViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="testuser1@example.com",
            username="testusername1",
            password="testpassword",
        )

    def test_post_signup_success(self):
        response = self.client.post(
            path=reverse("signup"),
            data=json.dumps(
                {
                    "email": "testuser2@example.com",
                    "username": "testusername2",
                    "password": "testpassword",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_signup_fail_invalid_password(self):
        response = self.client.post(
            path=reverse("signup"),
            data=json.dumps(
                {
                    "email": "testuser2@example.com",
                    "username": "testusername2",
                    "password": "1234",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_signup_fail_already_existing_email(self):
        response = self.client.post(
            path=reverse("signup"),
            data=json.dumps(
                {
                    "email": "testuser1@example.com",
                    "username": "testusername2",
                    "password": "1234",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_signup_fail_already_existing_username(self):
        response = self.client.post(
            path=reverse("signup"),
            data=json.dumps(
                {
                    "email": "testuser2@example.com",
                    "username": "testusername1",
                    "password": "1234",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
