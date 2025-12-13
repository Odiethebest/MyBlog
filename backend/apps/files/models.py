from django.db import models

class FileAsset(models.Model):
    file = models.FileField(upload_to="uploads/%Y/%m/")
    filename = models.CharField(max_length=255)
    size = models.PositiveIntegerField(default=0)
    content_type = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)