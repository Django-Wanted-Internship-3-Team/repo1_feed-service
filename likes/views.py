from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post

from .serializers import PostLikeIncrementSerializer


class LikesAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound("Post Not Found.")

    def post(self, request, content_id):
        post = self.get_post(content_id)
        like_count = post.like_count
        serializer = PostLikeIncrementSerializer(
            post,
            data={"like_count": like_count + 1},
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=200)
