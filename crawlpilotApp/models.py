from django.db import models

class CrawledURL(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    links = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class CrawlingStatus(models.Model):
    url = models.URLField()
    status = models.CharField(max_length=20)
    result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)