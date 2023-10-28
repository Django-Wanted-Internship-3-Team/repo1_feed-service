from rest_framework import serializers

from posts.models import HashTag


class StatisticsQuerySerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=["date", "hour"])
    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)
    hashtag = serializers.CharField(required=False)
    value = serializers.CharField(required=False)


class StatisticsListSerializer(serializers.Serializer):
    datetime = serializers.DateTimeField()
    count = serializers.IntegerField()


class HashTagRecommendListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = (
            "id",
            "name",
        )
