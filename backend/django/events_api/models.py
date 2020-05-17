from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    event_date = models.DateTimeField(null=False)
    notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("event_date", "created_at")

    def __str__(self):
        return f"{self.title}"
