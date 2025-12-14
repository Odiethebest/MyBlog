from django.urls import path
from .views import CategoryListAPI, TagListAPI, CategoryPostsAPI, TagPostsAPI

urlpatterns = [
    path("categories/", CategoryListAPI.as_view()),
    path("tags/", TagListAPI.as_view()),
    path("categories/<int:category_id>/posts/", CategoryPostsAPI.as_view()),
    path("tags/<int:tag_id>/posts/", TagPostsAPI.as_view()),
]