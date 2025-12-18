from django.urls import path
from .views import (
    MessageListCreateAPI,
    AdminCommentDeleteAPI,
    AdminPendingCommentListAPI,
    AdminApproveCommentAPI,
    AdminPendingMessageListAPI,
    AdminApproveMessageAPI,
)

urlpatterns = [
    # public
    path("messages/", MessageListCreateAPI.as_view()),

    # admin
    path("api/admin/comments/pending/", AdminPendingCommentListAPI.as_view()),
    path("api/admin/comments/<int:comment_id>/approve/", AdminApproveCommentAPI.as_view()),
    path("api/admin/comments/<int:comment_id>/", AdminCommentDeleteAPI.as_view()),

    path("api/admin/messages/pending/", AdminPendingMessageListAPI.as_view()),
    path("api/admin/messages/<int:message_id>/approve/", AdminApproveMessageAPI.as_view()),
]