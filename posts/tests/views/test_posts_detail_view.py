import uuid

from django.contrib.auth import get_user_model
from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import HashTag, Post

User = get_user_model()


class PostListViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # 테스트 사용자 생성
        cls.user = User.objects.create_user(username="testuser1", password="testpass1", email="test1@email.com")

        # 테스트 해시태그 생성
        cls.hashtag = HashTag.objects.create(name="hashtag1")

        # 테스트 게시물 생성 및 content_id 저장
        cls.content_ids = []

        # 테스트 게시물 생성
        for i in range(1, 6):
            post = Post.objects.create(
                content_id=uuid.uuid4(),
                user=cls.user,
                post_type="facebook",
                title=f"test title {i}",
                content=f"test content {i}",
                view_count=10 * i,
                like_count=5 * i,
                share_count=2 * i,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )
            post.hashtag.set([cls.hashtag])
            cls.content_ids.append(str(post.content_id))

    def setUp(self):
        pass

    def test_get_existing_post_content_id(self):
        response = self.client.get(
            path=reverse("post-detail", kwargs={"content_id": self.content_ids[0]}),
            data={"type": "all", "hashtag": self.hashtag.id, "ordering": "created_at", "search": ""},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_not_existing_post_content_id(self):
        non_existing_content_id = "00000000-0000-0000-0000-000000000001"
        response = self.client.get(
            path=reverse("post-detail", kwargs={"content_id": non_existing_content_id}),
            data={"type": "all", "hashtag": self.hashtag.id, "ordering": "created_at", "search": ""},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_increment_view_count(self):
        content_id = self.content_ids[0]

        # 현재 조회수 가져오기
        # 초기값 - 1 (조회와 동시에 count가 됨)
        post = Post.objects.get(content_id=content_id)
        initial_view_count = post.view_count - 1

        # 게시물 조회
        with transaction.atomic():
            response = self.client.get(
                path=reverse("post-detail", kwargs={"content_id": content_id}),
                data={"type": "all", "hashtag": self.hashtag.id, "ordering": "created_at", "search": ""},
            )

        # 조회수 업데이트 확인
        post.refresh_from_db()
        updated_view_count = post.view_count

        print("initial_view_count", initial_view_count)

        self.assertEqual(updated_view_count, initial_view_count + 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
