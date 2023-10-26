from django.urls import path

from common.views import QueryTestView

urlpatterns = [
    path("query/", QueryTestView.as_view(), name="query"),
]
