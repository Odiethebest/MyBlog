from django.db import models

class FriendLink(models.Model):
    name = models.CharField(max_length=80)
    url = models.URLField()
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)