from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content", "content_markdown", "created_at", "updated_at"]
        extra_kwargs = {f: {"required": False} for f in ["content", "content_markdown"]}