from rest_framework.serializers import ModelSerializer

from posts.models import Post


class PostLikeIncrementSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ("like_count",)
