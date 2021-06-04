from django.db import models


class Youtube(models.Model):
    # Youtube DB Schema
    video_id = models.CharField(max_length=150, unique=True)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=200)
    published_at = models.DateTimeField()
    thumbnail_url = models.CharField(max_length=150)

