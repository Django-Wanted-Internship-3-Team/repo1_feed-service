from rest_framework.serializers import ModelSerializer

from posts.models import Post


class PostLikeIncrementSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def save(self, **kwargs):
        return super().save(**kwargs)
