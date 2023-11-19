from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView

from likes.serializers import PostLikeIncrementSerializer
from posts.models import Post


class LikesAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="게시물에 좋아요",
        responses={
            HTTP_200_OK: openapi.Response(description="ok"),
            HTTP_401_UNAUTHORIZED: openapi.Response(description="unauthorized"),
        },
    )
    def post(self, request, content_id):
        post = get_object_or_404(Post, content_id=content_id)

        serializer = PostLikeIncrementSerializer(
            post,
            data={"like_count": post.like_count + 1},
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=200)
