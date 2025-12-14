from django.db import models

class Message(models.Model):
    author_name = models.CharField(max_length=64)
    author_email = models.EmailField(blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Message({self.author_name}, {self.created_at})"


class Comment(models.Model):
    post = models.ForeignKey("blog.Post", on_delete=models.CASCADE, related_name="comments")
    author_name = models.CharField(max_length=64)
    author_email = models.EmailField(blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ["created_at"]  # 评论一般按时间正序

    def __str__(self) -> str:
        return f"Comment(post={self.post_id}, author={self.author_name})"



