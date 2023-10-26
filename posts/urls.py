from django.urls import path

from posts.views import StatisticsListView

urlpatterns = [
    path("statistics/", StatisticsListView.as_view(), name="statistics"),
]
