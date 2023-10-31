from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post
from shares.serializers import PostShareCountIncrementSerializer


class SharesAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="게시물 좋아요",
        responses={
            status.HTTP_200_OK: openapi.Response(description="ok"),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description="unauthorized"),
        },
    )
    def post(self, request, content_id):
        """
        게시물(content_id)에 대해 공유 요청을 합니다.
        """

        post = get_object_or_404(Post, content_id=content_id)

        # TODO : how to increment share_count using serializer not passing data.
        serializer = PostShareCountIncrementSerializer(
            instance=post,
            data={
                "share_count": post.share_count + 1,
            },
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)
