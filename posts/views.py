from datetime import datetime, timedelta

from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncDay, TruncHour
from django.db.models.query import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.decorator import mandatories, optionals
from common.exceptions import InvalidParameterException, UnknownServerErrorException
from common.utils import get_before_week, get_now
from posts.models import HashTag, Post, PostHashtag
from posts.serializers import (
    HashTagRecommendListSerializer,
    StatisticsListSerializer,
    StatisticsQuerySerializer,
)


class StatisticsListView(APIView):
    # @TODO: IsAuthenticated로 변경 @SaJH
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="통계 정보를 조회",
        query_serializer=StatisticsQuerySerializer,
        responses={
            status.HTTP_200_OK: StatisticsListSerializer,
        },
    )
    @mandatories("type")
    @optionals({"start": get_before_week()}, {"end": get_now()}, {"hashtag": None}, {"value": "count"})
    def get(self, request: Request, m: dict, o: dict) -> Response:
        """
        query parameter로 type, start, end, hashtag, value를 받아 통계 정보를 조회합니다.

        Args:
            type: date, hour 중 하나를 선택합니다.
            start: 조회 시작 날짜입니다. (default: 7일 전)
            end: 조회 종료 날짜입니다. (default: 현재)
            hashtag: 조회할 해시태그입니다. (default: 본인계정)
            value: count, view_count, share_count, like_count 조회할 값입니다. (default: count)

        Returns:
            date: 날짜/시간
            count: 조회할 값의 수
        """
        try:
            # 쿼리 매개변수 받기
            date_type = m["type"]
            start_date, end_date, value = o["start"], o["end"], o["value"]
            hashtag = request.user.email if o["hashtag"] is None else o["hashtag"]

            # date type에 따른 필드, 기간, 집계 정보 가져오기
            max_days, aggregation_field, aggregation_type = self.get_aggregation_info(date_type)

            # date type에 따른 최대 기간 체크 or 날짜 데이터 타입 변환
            start_date, end_date = self.get_dates(date_type, max_days, start_date, end_date)

            # 필터링된 queryset 가져오기
            queryset = self.get_filtered_queryset(start_date, end_date, hashtag)

            # 집계 정보 가져오기
            statistics = self.get_statistics(queryset, aggregation_field, value, aggregation_type)

            # 집계 정보 serialize
            serializer = StatisticsListSerializer(statistics, many=True)
        except Exception as e:
            raise UnknownServerErrorException(e)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_aggregation_info(self, date_type: str) -> tuple:
        if date_type == "date":
            max_days = 30
            aggregation_field = "created_at"
            aggregation_type = TruncDay
        elif date_type == "hour":
            max_days = 7
            aggregation_field = "created_at"
            aggregation_type = TruncHour
        else:
            raise InvalidParameterException("type은 date, hour 중 선택 가능합니다.")
        return max_days, aggregation_field, aggregation_type

    def get_dates(self, date_type: str, max_days: int, start_date: str, end_date: str) -> None:
        if isinstance(start_date, str) and isinstance(end_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)

        if (end_date - start_date).days > max_days:
            raise InvalidParameterException(f"{date_type}는 최대 {max_days}일 조회 가능합니다.")

        return start_date, end_date

    def get_filtered_queryset(self, start_date: str, end_date: str, hashtag: str) -> Post:
        q = Q(created_at__range=(start_date, end_date)) & Q(hashtag_set__name=hashtag)
        return Post.objects.prefetch_related("hashtag_set").filter(q)

    def get_statistics(self, queryset: Post, aggregation_field: str, value: str, aggregation_type) -> QuerySet[dict]:
        if value == "count":
            statistics = queryset.annotate(datetime=aggregation_type(aggregation_field)).values("datetime").annotate(count=Count("id"))
        elif value in ["view_count", "like_count", "share_count"]:
            statistics = queryset.annotate(datetime=aggregation_type(aggregation_field)).values("datetime").annotate(count=Sum(value))
        else:
            raise InvalidParameterException("value는 count, view_count, share_count, like_count 중 선택 가능합니다.")
        return statistics


class HashTagRecommendListView(APIView):
    # @TODO: IsAuthenticated로 변경 @SaJH
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="최근 3시간 동안 가장 많이 사용된 Tag 조회",
        responses={
            status.HTTP_200_OK: HashTagRecommendListSerializer,
        },
    )
    def get(self, request: Request) -> Response:
        """
        최근 3시간 동안 가장 많이 사용된 Tag를 조회하는 API 입니다.

        Returns:
            hashtag_id: 해시태그 id
            hashtag_name: 해시태그 이름
        """
        try:
            today = datetime.now()
            three_hours_ago = today - timedelta(hours=3)
            queryset = self.get_filtered_queryset(today, three_hours_ago)
            serializer = HashTagRecommendListSerializer(queryset, many=True)
        except Exception as e:
            raise UnknownServerErrorException(e)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_filtered_queryset(self, today: str, three_hours_ago: str) -> PostHashtag:
        q = Q(posthashtag__created_at__range=(three_hours_ago, today))
        queryset = HashTag.objects.prefetch_related("posthashtag_set").filter(q).annotate(count=Count("posthashtag")).order_by("-count")
        return queryset
