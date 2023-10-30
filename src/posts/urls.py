from django.urls import path

from posts.views import PostListView, StatisticsListView

urlpatterns = [
    path("statistics/", StatisticsListView.as_view(), name="statistics"),
    path("", PostListView.as_view(), name="list"),
]
