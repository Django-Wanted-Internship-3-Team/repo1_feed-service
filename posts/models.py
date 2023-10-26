import uuid

from django.db import models

from users.models import User


class Post(models.Model):
    class PostType(models.TextChoices):
        FACEBOOK = "facebook"
        TWITTER = "twitter"
        INSTAGRAM = "instagram"
        THREADS = "threads"

    content_id = models.UUIDField(default=uuid.uuid4, editable=False)
    post_type = models.CharField(max_length=16, choices=PostType.choices)
    title = models.CharField(max_length=32)
    content = models.TextField()
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    hashtag = models.ManyToManyField("HashTag", related_name="posts")

    class Meta:
        db_table = "posts"

    def __str__(self):
        return f"{self.title} by {self.user.email}"


class HashTag(models.Model):
    name = models.CharField(max_length=32)
    hashtag_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "hashtag"

    def __str__(self):
        return self.name
