from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response

from apps.blog.models import Post
from .models import Comment, Message
from .serializers import CommentSerializer, MessageSerializer
from .pagination import StandardPagination


class PostCommentListCreateAPI(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = StandardPagination
    permission_classes = [permissions.AllowAny]

    def _get_post(self):
        # 统一在 GET/POST 都校验 post 是否存在
        return get_object_or_404(Post, id=self.kwargs["post_id"])

    def get_queryset(self):
        # 先校验 post 存在；不存在就直接 404（而不是返回空列表）
        self._get_post()

        post_id = self.kwargs["post_id"]
        return (
            Comment.objects
            .filter(post_id=post_id, is_approved=True)
            .order_by("created_at")
        )

    def list(self, request, *args, **kwargs):
        # 同样保证 list 时 post 必须存在
        post = self._get_post()
        qs = self.get_queryset()

        page = self.paginate_queryset(qs)
        ser = self.get_serializer(page, many=True)
        p = self.paginator

        return Response({
            "post_id": post.id,
            "page": p.page.number,
            "page_size": p.get_page_size(request),
            "total": qs.count(),
            "comments": ser.data,
        })

    def perform_create(self, serializer):
        post = self._get_post()
        serializer.save(post=post)


class MessageListCreateAPI(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    pagination_class = StandardPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Message.objects.filter(is_approved=True).order_by("-created_at")

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        ser = self.get_serializer(page, many=True)
        p = self.paginator
        return Response({
            "page": p.page.number,
            "page_size": p.get_page_size(request),
            "total": qs.count(),
            "messages": ser.data,
        })


class AdminCommentDeleteAPI(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = "comment_id"
    permission_classes = [permissions.IsAdminUser]