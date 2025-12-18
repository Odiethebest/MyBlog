from django.urls import path
from .views import (
    PostCommentListCreateAPI,
    MessageListCreateAPI,
    AdminCommentDeleteAPI,
    AdminPendingCommentListAPI,
    AdminApproveCommentAPI,
    AdminPendingMessageListAPI,
    AdminApproveMessageAPI,
)

urlpatterns = [
    # public (mounted under /api/)
    path("blog/<int:post_id>/comments/", PostCommentListCreateAPI.as_view(), name="post-comments"),
    path("messages/", MessageListCreateAPI.as_view(), name="messages"),

    # admin (final: /api/admin/...)
    path("admin/comments/pending/", AdminPendingCommentListAPI.as_view(), name="admin-comments-pending"),
    path("admin/comments/<int:comment_id>/approve/", AdminApproveCommentAPI.as_view(), name="admin-comment-approve"),
    path("admin/comments/<int:comment_id>/", AdminCommentDeleteAPI.as_view(), name="admin-comment-delete"),

    path("admin/messages/pending/", AdminPendingMessageListAPI.as_view(), name="admin-messages-pending"),
    path("admin/messages/<int:message_id>/approve/", AdminApproveMessageAPI.as_view(), name="admin-message-approve"),
]