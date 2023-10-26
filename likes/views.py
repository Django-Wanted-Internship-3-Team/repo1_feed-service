from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post

from .serializers import PostLikeIncrementSerializer


class LikesAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

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
