from django.urls import path
from .query_views import (
    BlogSearchView,
    CategoryListView, CategoryPostsView,
    TagListView, TagPostsView,
    ArchiveMonthsView, ArchivePostsView,
)

urlpatterns = [
    path("blog/search/", BlogSearchView.as_view(), name="blog-search"),

    path("categories/", CategoryListView.as_view(), name="categories"),
    path("categories/<int:category_id>/posts/", CategoryPostsView.as_view(), name="category-posts"),

    path("tags/", TagListView.as_view(), name="tags"),
    path("tags/<int:tag_id>/posts/", TagPostsView.as_view(), name="tag-posts"),

    path("archives/", ArchiveMonthsView.as_view(), name="archives"),
    path("archives/<int:year>/<int:month>/posts/", ArchivePostsView.as_view(), name="archive-posts"),
]