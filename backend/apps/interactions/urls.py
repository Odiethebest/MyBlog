from django.urls import path
from .views import PostCommentListCreateAPI, MessageListCreateAPI, AdminCommentDeleteAPI, AdminCommentApproveAPI

urlpatterns = [
    path("blog/<int:post_id>/comments/", PostCommentListCreateAPI.as_view()),
    path("messages/", MessageListCreateAPI.as_view()),

    # admin
    path("api/admin/comments/<int:comment_id>/", AdminCommentDeleteAPI.as_view()),
    path("api/admin/comments/<int:comment_id>/approve/", AdminCommentApproveAPI.as_view()),
]