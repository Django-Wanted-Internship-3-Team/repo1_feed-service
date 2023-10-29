from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post


class SharesAPITestCase(APITestCase):
    """
    /shares/<content_id>/ post 에 대한 테스트 케이스
    """

    viewname = "shares"

    def test_post_failure_no_api(self):
        """
        해당 view가 없으면 NoReverseMatch 예외가 수반됩니다.
        """
        reverse(self.viewname, kwargs={"content_id": None})

    def test_post_without_auth(self):
        """
        인증되지 않은 사용자가 shares에 post 요청을 전달하고,
        401(unauth) 응답을 얻습니다.
        """

        post = Post.objects.create(title="title")
        self.client.logout()
        response = self.client.post(
            path=reverse(self.viewname, kwargs={"content_id": post.content_id}),
            data=None,
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # status 401

    def test_post_with_auth(self):
        """
        인증된 사용자가 shares에 post 요청을 전달하고,
        200(Ok) 응답을 얻으며 share_count가 증가합니다.
        """

        post = Post.objects.create(title="title")

        user = get_user_model().objects.create(username="username")
        self.client.force_authenticate(user=user)

        response = self.client.post(
            path=reverse(self.viewname, kwargs={"content_id": post.content_id}),
            data=None,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # status 200

        post_after_response = Post.objects.get(content_id=post.content_id)
        self.assertEqual(post.share_count + 1, post_after_response.share_count)  # share_count diff 1
