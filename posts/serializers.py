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
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        return obj.content[:20] if obj.content else ""

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


class PostQuerySerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=["all", "facebook", "twitter", "instagram", "threads"],
        required=False,
        default="all",
        help_text="게시물 타입 중 하나를 선택하여 조회합니다. (default: 모든 게시물 타입)",
    )
    search = serializers.CharField(required=False, help_text="title, content, title + content 내에 존재하는 키워드를 검색하여 일치하는 데이터들을 조회합니다.")
    ordering = serializers.ChoiceField(
        choices=[
            "created_at",
            "updated_at",
            "view_count",
            "like_count",
            "share_count",
            "-created_at",
            "-updated_at",
            "-view_count",
            "-like_count",
            "-share_count",
        ],
        required=False,
        default="created_at",
        help_text="created_at, updated_at, view_count, like_count, share_count를 기준으로 오름차순/내림차순으로 정렬하여 조회합니다. (default: created_at)",
    )
    hashtag = serializers.CharField(required=False, help_text="조회할 해시태그입니다. (default: 본인계정)")


class PostDetailSerializer(serializers.ModelSerializer):
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


class PostDetailQuerySerializer(serializers.Serializer):
    content_id = serializers.UUIDField()
