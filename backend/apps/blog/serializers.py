from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    # 对外统一用 content；读写都走 content_markdown
    content = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Post
        # ✅ 对外只暴露 content，不暴露 content_markdown（避免重复字段）
        fields = ["id", "title", "content", "created_at", "updated_at"]
        extra_kwargs = {
            "title": {"required": True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["content"] = instance.content_markdown or ""
        return data

    def create(self, validated_data):
        # 兼容：外部传 content 或 content_markdown 都可以
        content = validated_data.pop("content", None)
        if content is None and "content_markdown" in validated_data:
            content = validated_data.pop("content_markdown")
        validated_data["content_markdown"] = content or ""
        return super().create(validated_data)

    def update(self, instance, validated_data):
        content = validated_data.pop("content", None)
        if content is None and "content_markdown" in validated_data:
            content = validated_data.pop("content_markdown")
        if content is not None:
            instance.content_markdown = content
        # 其他字段正常更新（title等）
        return super().update(instance, validated_data)