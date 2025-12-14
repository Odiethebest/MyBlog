from django.urls import path
from .views import PostCommentListCreateAPI, MessageListCreateAPI, AdminCommentDeleteAPI

urlpatterns = [
    path("blog/<int:post_id>/comments/", PostCommentListCreateAPI.as_view()),
    path("messages/", MessageListCreateAPI.as_view()),
    path("admin/comments/<int:comment_id>/", AdminCommentDeleteAPI.as_view()),
]