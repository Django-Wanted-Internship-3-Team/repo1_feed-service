from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class QueryTest(APITestCase):
    def test_get_query(self):
        response = self.client.get(
            path=reverse("query"),
            data={
                "name": "John",
                "age": "30",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "John")
        self.assertEqual(response.data["age"], "30")

    def test_post_query(self):
        response = self.client.post(
            path=reverse("query"),
            data={
                "city": "New York",
                "occupation": "Engineer",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["city"], "New York")
        self.assertEqual(response.data["occupation"], "Engineer")

    def test_query_fail(self):
        response = self.client.get(
            path=reverse("query"),
            data={
                "name": "John",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
