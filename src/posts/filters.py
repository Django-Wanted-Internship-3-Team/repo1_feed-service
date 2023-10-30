import django_filters

from .models import Post


class PostFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        fields=(
            ("created_at", "created_at"),
            ("-created_at", "-created_at"),
            ("updated_at", "updated_at"),
            ("-updated_at", "-updated_at"),
            ("view_count", "view_count"),
            ("-view_count", "-view_count"),
            ("share_count", "share_count"),
            ("-share_count", "-share_count"),
            ("like_count", "like_count"),
            ("-like_count", "-like_count"),
        ),
        field_name="ordering",
        help_text="정렬 기준과 방향",
    )

    class Meta:
        model = Post
        fields = ["ordering"]
