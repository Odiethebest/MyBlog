from collections import defaultdict
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .memory_store import POSTS, CATEGORIES, TAGS
from .pagination import parse_pagination_params, paginate


def _post_list_item(post):
    # 用于列表页：只返回 README 示例里那几个字段（更接近真实）
    return {
        "id": post["id"],
        "title": post["title"],
        "excerpt": post.get("excerpt", "")[:200],
        "author": post.get("author", "odie"),
        "created_at": post.get("created_at"),
        "tags": post.get("tags", []),
        "category": post.get("category", {}).get("name") if post.get("category") else None,
    }


class BlogSearchView(APIView):
    def get(self, request):
        q = (request.query_params.get("q") or "").strip()
        page, page_size = parse_pagination_params(request.query_params)

        def match(p):
            if not q:
                return True
            text = (p.get("title", "") + " " + p.get("content", "")).lower()
            return q.lower() in text

        filtered = [p for p in POSTS if match(p)]
        # created_at 倒序（字符串 ISO8601 直接比较也基本可用；我们简单处理）
        filtered = sorted(filtered, key=lambda x: x.get("created_at") or "", reverse=True)

        items, total = paginate([_post_list_item(p) for p in filtered], page, page_size)
        return Response(
            {"query": q, "page": page, "page_size": page_size, "total": total, "posts": items},
            status=status.HTTP_200_OK,
        )


class CategoryListView(APIView):
    def get(self, request):
        result = []
        for c in CATEGORIES:
            count = sum(1 for p in POSTS if p.get("category", {}).get("id") == c["id"])
            result.append({**c, "post_count": count})
        return Response({"categories": result}, status=status.HTTP_200_OK)


class CategoryPostsView(APIView):
    def get(self, request, category_id: int):
        page, page_size = parse_pagination_params(request.query_params)

        category = next((c for c in CATEGORIES if c["id"] == category_id), None)
        if not category:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        filtered = [p for p in POSTS if p.get("category", {}).get("id") == category_id]
        filtered = sorted(filtered, key=lambda x: x.get("created_at") or "", reverse=True)

        posts, total = paginate(
            [{"id": p["id"], "title": p["title"], "excerpt": p.get("excerpt", "")[:200], "created_at": p.get("created_at")} for p in filtered],
            page, page_size
        )

        return Response(
            {"category": category, "page": page, "page_size": page_size, "total": total, "posts": posts},
            status=status.HTTP_200_OK,
        )


class TagListView(APIView):
    def get(self, request):
        result = []
        for t in TAGS:
            count = sum(1 for p in POSTS if t["name"] in (p.get("tags") or []))
            result.append({**t, "post_count": count})
        return Response({"tags": result}, status=status.HTTP_200_OK)


class TagPostsView(APIView):
    def get(self, request, tag_id: int):
        page, page_size = parse_pagination_params(request.query_params)

        tag = next((t for t in TAGS if t["id"] == tag_id), None)
        if not tag:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        filtered = [p for p in POSTS if tag["name"] in (p.get("tags") or [])]
        filtered = sorted(filtered, key=lambda x: x.get("created_at") or "", reverse=True)

        posts, total = paginate(
            [{"id": p["id"], "title": p["title"], "excerpt": p.get("excerpt", "")[:200], "created_at": p.get("created_at")} for p in filtered],
            page, page_size
        )

        return Response(
            {"tag": tag, "page": page, "page_size": page_size, "total": total, "posts": posts},
            status=status.HTTP_200_OK,
        )


class ArchiveMonthsView(APIView):
    def get(self, request):
        buckets = defaultdict(int)
        for p in POSTS:
            created = p.get("created_at")
            if not created:
                continue
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            buckets[(dt.year, dt.month)] += 1

        archives = [{"year": y, "month": m, "post_count": cnt} for (y, m), cnt in buckets.items()]
        archives.sort(key=lambda x: (x["year"], x["month"]), reverse=True)
        return Response({"archives": archives}, status=status.HTTP_200_OK)


class ArchivePostsView(APIView):
    def get(self, request, year: int, month: int):
        page, page_size = parse_pagination_params(request.query_params)

        def in_month(p):
            created = p.get("created_at")
            if not created:
                return False
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            return dt.year == year and dt.month == month

        filtered = [p for p in POSTS if in_month(p)]
        filtered = sorted(filtered, key=lambda x: x.get("created_at") or "", reverse=True)

        posts, total = paginate(
            [{"id": p["id"], "title": p["title"], "excerpt": p.get("excerpt", "")[:200], "created_at": p.get("created_at")} for p in filtered],
            page, page_size
        )

        return Response(
            {"archive": {"year": year, "month": month}, "page": page, "page_size": page_size, "total": total, "posts": posts},
            status=status.HTTP_200_OK,
        )