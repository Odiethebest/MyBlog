from django.db import models

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=80, default="MyBlog")
    site_description = models.CharField(max_length=200, default="")
    comment_enabled = models.BooleanField(default=True)
    maintenance_mode = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)