from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source="content_markdown", required=False, allow_blank=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "content_markdown", "created_at", "updated_at"]
        extra_kwargs = {
            "content_markdown": {"required": False, "allow_blank": True},
            "title": {"required": True},
        }

    def validate(self, attrs):
        return attrs