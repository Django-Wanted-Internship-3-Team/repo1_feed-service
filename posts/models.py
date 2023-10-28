import uuid

from django.db import models


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
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    hashtag_set = models.ManyToManyField("HashTag", through="PostHashtag", through_fields=("post", "hashtag"))

    class Meta:
        db_table = "posts"

    def __str__(self):
        return f"[{self.user.email}]: {self.title}"


class HashTag(models.Model):
    name = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "hashtags"

    def __str__(self):
        return self.name


class PostHashtag(models.Model):
    post = models.ForeignKey("Post", on_delete=models.SET_NULL, null=True)
    hashtag = models.ForeignKey("HashTag", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "posts_hashtags"
        unique_together = ("post", "hashtag")

    def __str__(self):
        return f"{self.post.title} - {self.hashtag.name}"
