from django.db.models.signals import pre_save
from django.dispatch import receiver

from posts.models import Post


@receiver(pre_save, sender=Post)
def increment_view_count(sender, instance, **kwargs):
    # 게시글을 조회할 때 조회수 증가
    instance.view_count += 1
