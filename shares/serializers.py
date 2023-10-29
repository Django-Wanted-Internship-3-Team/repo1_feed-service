from rest_framework.serializers import ModelSerializer

from posts.models import Post


class PostShareCountIncrementSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ("share_count",)
