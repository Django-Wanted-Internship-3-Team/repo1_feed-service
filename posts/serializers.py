from rest_framework import serializers

from .models import HashTag, Post


class StatisticsQuerySerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=["date", "hour"])
    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)
    hashtag = serializers.CharField(required=False)
    value = serializers.CharField(required=False)


class StatisticsListSerializer(serializers.Serializer):
    datetime = serializers.DateTimeField()
    count = serializers.IntegerField()


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = [
            "name",
        ]


class PostListSerializer(serializers.ModelSerializer):
    hashtag = HashTagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "content_id",
            "post_type",
            "title",
            "content",
            "view_count",
            "like_count",
            "share_count",
            "created_at",
            "updated_at",
            "hashtag",
            "user",
        ]
