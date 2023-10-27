from datetime import datetime, timedelta

from django.db.models import Count, F, Q, Sum
from django.db.models.functions import TruncDay, TruncHour
from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.decorator import mandatories, optionals
from common.exceptions import InvalidParameterException, UnknownServerErrorException
from common.utils import get_before_week, get_now
from posts.filters import PostFilter
from posts.models import Post
from posts.paginations import PaginationHandlerMixin
from posts.serializers import PostListSerializer, StatisticsListSerializer, StatisticsQuerySerializer


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
        q = Q(created_at__range=(start_date, end_date)) & Q(hashtag__name=hashtag)
        return Post.objects.prefetch_related("hashtag").filter(q)

    def get_statistics(self, queryset: Post, aggregation_field: str, value: str, aggregation_type) -> QuerySet[dict]:
        if value == "count":
            statistics = queryset.annotate(datetime=aggregation_type(aggregation_field)).values("datetime").annotate(count=Count("id"))
        elif value in ["view_count", "like_count", "share_count"]:
            statistics = queryset.annotate(datetime=aggregation_type(aggregation_field)).values("datetime").annotate(count=Sum(value))
        else:
            raise InvalidParameterException("value는 count, view_count, share_count, like_count 중 선택 가능합니다.")
        return statistics


class PostListView(PaginationHandlerMixin, APIView):
    # @TODO: IsAuthenticated로 변경 @simseulnyang
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["ordering"]
    filterset_class = PostFilter
    pagination_class = LimitOffsetPagination

    @swagger_auto_schema(
        operation_summary="게시물 리스트를 조회",
        query_serializer=PostListSerializer,
        responses={
            status.HTTP_200_OK: PostListSerializer,
        },
    )
    @mandatories("type")
    @optionals({"hashtag": None})
    def get(self, request: Request, m: dict, o: dict) -> Response:
        """
        query parameter로 type, search, ordering, hashtag를 받아 게시물 목록을 조회합니다.

        Args:
            type: 게시물 타입으로 facebook, twitter, instagram, threads 중에 1개를 선택하여 조회 가능합니다. (default : 모든 게시물 타입)
            hashtag: 조회할 해시태그입니다. (default: 본인계정)

        Returns:
            content_id : 게시물 id
            hashtag : 해시태그
            user : 게시글 작성 유저
            post_type : 게시물 타입
            title : 게시글 제목
            content : 게시글 내용
            view_count : 조회수
            like_count : 좋아요 수
            share_count : 공유 수
            created_at : 작성일자
            updated_at : 업데이트 일자
        """
        try:
            # 쿼리 매개변수 받기
            post_type = m["type"]
            search_keyword = request.query_params.get("search", "")
            hashtag = request.user.username if o["hashtag"] is None else o["hashtag"]

            # 유저 계정의 해시태그로 초기 필터링한 게시물 목록 가져오기
            postlist = Post.objects.filter(user__username=hashtag)

            # 검색어로 필터링
            if search_keyword:
                postlist = postlist.filter(Q(title__icontains=search_keyword).distinct() | Q(content__icontains=search_keyword).distinct())

            # 사용자 정의 정렬 필터 적용
            filter = PostFilter(request.GET, queryset=postlist)
            postlist = filter.qs

            # post_type에 따라 필터링 된 게시물 목록 가져오기
            post_type_list = self.get_post_type_list(postlist, post_type)

            # 게시물 목록 serialize
            serializer = PostListSerializer(post_type_list, many=True)
        except Exception as e:
            raise UnknownServerErrorException(e)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def apply_ordering(self, postlist, ordering):
        """
        정렬 기준을 적용하여 postlist 정렬합니다.
        ordering에 "asc" 또는 "desc"를 추가하여 오름차순 또는 내림차순 정렬 가능합니다.

        Args:
            postlist: 정렬할 postlist
            ordering: 정렬 기준과 방향 (예: created_at:desc)

        Returns:
            정렬된 postlist
        """
        ordering_parts = ordering.split(":")
        field_name = ordering_parts[0]
        direction = ordering_parts[1] if len(ordering_parts) > 1 else "desc"

        if direction == "asc":
            field_name = F(field_name).asc()
        else:
            field_name = F(field_name).desc()

        return postlist.order_by(field_name)

    def get_post_type_list(self, postlist: Post, post_type: str):
        if post_type == "facebook":
            post_type_list = postlist.filter(post_type="facebook")
        elif post_type == "twitter":
            post_type_list = postlist.filter(post_type="twitter")
        elif post_type == "instagram":
            post_type_list = postlist.filter(post_type="instagram")
        elif post_type == "threads":
            post_type_list = postlist.filter(post_type="threads")
        else:
            raise InvalidParameterException("post_type 값을 잘못 선택하셨습니다.")
        return post_type_list
