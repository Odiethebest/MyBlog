from typing import Dict, List

POSTS: List[Dict] = [
    {"id": 1, "title": "First Post", "content": "This is the content of the first post."},
    {"id": 2, "title": "Second Post", "content": "This is the content of the second post."},
]

def next_id() -> int:
    return max((p["id"] for p in POSTS), default=0) + 1

def find_post(post_id: int):
    for p in POSTS:
        if p["id"] == post_id:
            return p
    return None