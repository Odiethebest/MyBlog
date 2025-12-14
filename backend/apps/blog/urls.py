from django.urls import path
from .views import BlogListCreateView, BlogRetrieveUpdateDeleteView
from .views import BlogSearchAPI, ArchiveMonthsAPI, ArchivePostsAPI
urlpatterns = [
    path("", BlogListCreateView.as_view(), name="blog-list-create"),
    path("<int:post_id>/", BlogRetrieveUpdateDeleteView.as_view(), name="blog-rud"),
    path("blog/search/", BlogSearchAPI.as_view()),
    path("archives/", ArchiveMonthsAPI.as_view()),
    path("archives/<int:year>/<int:month>/posts/", ArchivePostsAPI.as_view()),
]