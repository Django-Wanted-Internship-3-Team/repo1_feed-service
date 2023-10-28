from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import HashTag, Post

User = get_user_model()


class PostListViewTest(APITestCase):
    def setUp(self):
        # 테스트 사용자 생성
        self.user1 = User.objects.create_user(username="testuser1", password="testpass1", email="test1@email.com")
        self.user2 = User.objects.create_user(username="testuser2", password="testpass2", email="test2@email.com")

        # 테스트 해시태그 생성
        self.hashtag1 = HashTag.objects.create(name="hashtag1")
        self.hashtag2 = HashTag.objects.create(name="hashtag2")

        # 테스트 게시물 생성
        self.post1 = Post.objects.create(
            user=self.user1,
            post_type="facebook",
            title="test title 1",
            content="test content 1",
            view_count=10,
            like_count=5,
            share_count=2,
        )
        self.post1.hashtag.set([self.hashtag1])

        self.post2 = Post.objects.create(
            user=self.user2,
            post_type="twitter",
            title="test title 2",
            content="test content 2",
            view_count=20,
            like_count=10,
            share_count=4,
        )
        self.post2.hashtag.set([self.hashtag2])

        # 추가 게시물 생성
        for i in range(3, 6):
            post = Post.objects.create(
                user=self.user1,
                post_type="facebook",
                title=f"test title {i}",
                content=f"test content {i}",
                view_count=10 * i,
                like_count=5 * i,
                share_count=2 * i,
            )
            post.hashtag.set([self.hashtag1])

    def test_get_posts_list_success(self):
        response = self.client.get(
            path=reverse("list"),
            data={"type": "all", "hashtag": self.hashtag1.id, "ordering": "created_at", "search": ""},
        )
        print(response.data)  # 서버의 응답 내용 출력
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # 예상되는 게시물 개수 확인
        for item in response.data:
            self.assertEqual(item["hashtag"][0]["name"], self.hashtag1.name)  # 수정된 부분

    def test_get_posts_list_invalid_type(self):
        response = self.client.get(
            path=reverse("list"),
            data={"type": "invalid_type", "hashtag": "hashtag", "ordering": "created_at", "search": ""},  # 잘못된 타입
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_posts_list_invalid_ordering(self):
        response = self.client.get(
            path=reverse("list"),
            data={"type": "all", "hashtag": "hashtag", "ordering": "invalid_ordering", "search": ""},  # 잘못된 ordering 값
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
