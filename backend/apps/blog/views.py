from django.db.models import Q, Count
from django.db.models.functions import ExtractYear, ExtractMonth

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer
from apps.taxonomy.pagination import StandardPagination  # 复用分页


def _excerpt(text: str, n: int = 120) -> str:
    if not text:
        return ""
    text = " ".join(text.split())
    return text[:n] + ("..." if len(text) > n else "")


def _content_of(p: Post) -> str:
    # 你的模型是 content_markdown / excerpt / content_html
    return (getattr(p, "content_markdown", "") or getattr(p, "excerpt", "") or getattr(p, "content_html", "") or "")


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    GET/HEAD/OPTIONS 允许所有人
    POST/PUT/PATCH/DELETE 仅管理员
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly]


class BlogRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = "post_id"
    permission_classes = [IsAdminOrReadOnly]


class BlogSearchAPI(APIView):
    pagination_class = StandardPagination

    def get(self, request):
        q = (request.query_params.get("q") or "").strip()
        qs = Post.objects.all()

        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(content_markdown__icontains=q) |
                Q(excerpt__icontains=q) |
                Q(content_html__icontains=q)
            )

        qs = qs.order_by("-created_at").distinct()

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)

        posts = []
        for p in page:
            tags = list(p.tags.values_list("name", flat=True)) if hasattr(p, "tags") else []
            category_name = p.category.name if getattr(p, "category", None) else None

            posts.append({
                "id": p.id,
                "title": p.title,
                "excerpt": _excerpt(_content_of(p)),
                "author": getattr(getattr(p, "author", None), "username", None) or "odie",
                "created_at": p.created_at,
                "tags": tags,
                "category": category_name,
            })

        payload = paginator.get_paginated_payload(
            extra={"query": q},
            items={"posts": posts},
        )
        return Response(payload)


class ArchiveMonthsAPI(APIView):
    def get(self, request):
        qs = (
            Post.objects
            .annotate(year=ExtractYear("created_at"), month=ExtractMonth("created_at"))
            .values("year", "month")
            .annotate(post_count=Count("id"))
            .order_by("-year", "-month")
        )
        return Response({"archives": list(qs)})


class ArchivePostsAPI(APIView):
    pagination_class = StandardPagination

    def get(self, request, year: int, month: int):
        qs = Post.objects.filter(created_at__year=year, created_at__month=month).order_by("-created_at")

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)

        posts = []
        for p in page:
            posts.append({
                "id": p.id,
                "title": p.title,
                "excerpt": _excerpt(_content_of(p)),
                "created_at": p.created_at,
            })

        payload = paginator.get_paginated_payload(
            extra={"archive": {"year": year, "month": month}},
            items={"posts": posts},
        )
        return Response(payload)