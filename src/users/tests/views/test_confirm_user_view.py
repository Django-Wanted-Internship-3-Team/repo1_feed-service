import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User, UserConfirmCode


class SignupViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="testuser1@example.com",
            username="testusername1",
            password="testpassword",
        )

        cls.userconfirmcode = UserConfirmCode.objects.create(
            code="abcdef",
            user=cls.user,
        )

    def test_post_signup_success(self):
        response = self.client.post(
            path=reverse("confirm"),
            data=json.dumps(
                {
                    "username": "testusername1",
                    "password": "testpassword",
                    "code": "abcdef",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_signup_fail_user_not_found(self):
        response = self.client.post(
            path=reverse("confirm"),
            data=json.dumps(
                {
                    "username": "testusername2",
                    "password": "testpassword",
                    "code": "abcdef",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_signup_fail_invalid_password(self):
        response = self.client.post(
            path=reverse("confirm"),
            data=json.dumps(
                {
                    "username": "testusername1",
                    "password": "testpassword2",
                    "code": "abcdef",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_signup_fail_invalid_code(self):
        response = self.client.post(
            path=reverse("confirm"),
            data=json.dumps(
                {
                    "username": "testusername1",
                    "password": "testpassword",
                    "code": "aaaaaa",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_signup_fail_already_confirmed(self):
        self.user.is_confirmed = True
        self.user.save()
        response = self.client.post(
            path=reverse("confirm"),
            data=json.dumps(
                {
                    "username": "testusername1",
                    "password": "testpassword",
                    "code": "abcdef",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
