from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .memory_store import POSTS, next_id, find_post


class BlogListCreateView(APIView):
    def get(self, request):
        return Response({"posts": POSTS}, status=status.HTTP_200_OK)

    def post(self, request):
        title = (request.data.get("title") or "").strip()
        content = (request.data.get("content") or "").strip()
        if not title or not content:
            return Response({"detail": "title and content are required"}, status=status.HTTP_400_BAD_REQUEST)

        post = {"id": next_id(), "title": title, "content": content}
        POSTS.append(post)
        return Response(post, status=status.HTTP_201_CREATED)


class BlogRetrieveUpdateDeleteView(APIView):
    def get(self, request, post_id: int):
        post = find_post(post_id)
        if not post:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(post, status=status.HTTP_200_OK)

    def put(self, request, post_id: int):
        post = find_post(post_id)
        if not post:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        title = (request.data.get("title") or "").strip()
        content = (request.data.get("content") or "").strip()
        if not title or not content:
            return Response({"detail": "title and content are required"}, status=status.HTTP_400_BAD_REQUEST)

        post["title"] = title
        post["content"] = content
        return Response(post, status=status.HTTP_200_OK)

    def delete(self, request, post_id: int):
        post = find_post(post_id)
        if not post:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        POSTS.remove(post)
        return Response(status=status.HTTP_204_NO_CONTENT)