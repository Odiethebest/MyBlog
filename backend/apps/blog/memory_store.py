from typing import Dict, List
from datetime import datetime, timezone

CATEGORIES = [
    {"id": 1, "name": "Backend", "slug": "backend"},
    {"id": 2, "name": "ML", "slug": "ml"},
]

TAGS = [
    {"id": 1, "name": "django", "slug": "django"},
    {"id": 2, "name": "drf", "slug": "drf"},
    {"id": 3, "name": "mysql", "slug": "mysql"},
]

def _dt(y, m, d, hh=10, mm=0, ss=0):
    return datetime(y, m, d, hh, mm, ss, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")

POSTS: List[Dict] = [
    {
        "id": 1,
        "title": "First Post",
        "content": "This is the content of the first post.",
        "excerpt": "This is the content of the first post.",
        "author": "odie",
        "created_at": _dt(2025, 12, 1, 10, 21, 12),
        "category": {"id": 1, "name": "Backend", "slug": "backend"},
        "tags": ["django", "drf"],
    },
    {
        "id": 2,
        "title": "Second Post",
        "content": "This is the content of the second post.",
        "excerpt": "This is the content of the second post.",
        "author": "odie",
        "created_at": _dt(2025, 11, 20, 9, 0, 0),
        "category": {"id": 2, "name": "ML", "slug": "ml"},
        "tags": ["mysql"],
    },
]

def next_id() -> int:
    return max((p["id"] for p in POSTS), default=0) + 1

def find_post(post_id: int):
    for p in POSTS:
        if p["id"] == post_id:
            return p
    return None