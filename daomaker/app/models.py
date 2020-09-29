from django.db import models
from django.utils import timezone


class Task(models.Model):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    site_name = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateField(default=timezone.now)

    def __str__(self):
        return self.url
