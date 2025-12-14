from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.blog.models import Post
from .models import Category, Tag
from .serializers import CategoryListSerializer, TagListSerializer
from .pagination import StandardPagination


def _excerpt(text: str, n: int = 120) -> str:
    if not text:
        return ""
    text = " ".join(text.split())
    return text[:n] + ("..." if len(text) > n else "")


class CategoryListAPI(APIView):
    def get(self, request):
        qs = Category.objects.annotate(post_count=Count("posts")).order_by("name")
        data = CategoryListSerializer(qs, many=True).data
        return Response({"categories": data})


class TagListAPI(APIView):
    def get(self, request):
        qs = Tag.objects.annotate(post_count=Count("posts")).order_by("name")
        data = TagListSerializer(qs, many=True).data
        return Response({"tags": data})


class CategoryPostsAPI(APIView):
    pagination_class = StandardPagination

    def get(self, request, category_id: int):
        category = get_object_or_404(Category, id=category_id)
        qs = Post.objects.filter(category=category).order_by("-created_at")

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)

        posts = []
        for p in page:
            # 你 Post 里字段如果叫 content_markdown，就把 p.content 改成 p.content_markdown
            posts.append({
                "id": p.id,
                "title": p.title,
                "excerpt": _excerpt(getattr(p, "content", "") or getattr(p, "content_markdown", "")),
                "created_at": p.created_at,
            })

        payload = paginator.get_paginated_payload(
            extra={"category": {"id": category.id, "name": category.name, "slug": category.slug}},
            items={"posts": posts},
        )
        return Response(payload)


class TagPostsAPI(APIView):
    pagination_class = StandardPagination

    def get(self, request, tag_id: int):
        tag = get_object_or_404(Tag, id=tag_id)
        qs = Post.objects.filter(tags=tag).order_by("-created_at").distinct()

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)

        posts = []
        for p in page:
            posts.append({
                "id": p.id,
                "title": p.title,
                "excerpt": _excerpt(getattr(p, "content", "") or getattr(p, "content_markdown", "")),
                "created_at": p.created_at,
            })

        payload = paginator.get_paginated_payload(
            extra={"tag": {"id": tag.id, "name": tag.name, "slug": tag.slug}},
            items={"posts": posts},
        )
        return Response(payload)