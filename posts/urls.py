from django.urls import path

from posts.views import HashTagRecommendListView, StatisticsListView

urlpatterns = [
    path("statistics/", StatisticsListView.as_view(), name="statistics_list"),
    path("hashtag/recommend/", HashTagRecommendListView.as_view(), name="hashtag_recommend_list"),
]
