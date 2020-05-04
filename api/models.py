from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
