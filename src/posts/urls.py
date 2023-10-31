from django.urls import path

from posts.views import PostDetailView, PostListView, StatisticsListView

urlpatterns = [
    path("statistics/", StatisticsListView.as_view(), name="statistics"),
    path("", PostListView.as_view(), name="list"),
    path("<str:content_id>/", PostDetailView.as_view(), name="post-detail"),
]
