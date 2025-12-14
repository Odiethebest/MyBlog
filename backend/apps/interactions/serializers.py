from rest_framework import serializers
from .models import Comment, Message

class CommentSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source="post.id", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post_id", "author_name", "author_email", "content", "created_at"]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "author_name", "author_email", "content", "created_at"]