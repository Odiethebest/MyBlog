from django.contrib import admin
from django.urls import path, include
from apps.blog.views import BlogSearchAPI, ArchiveMonthsAPI, ArchivePostsAPI

urlpatterns = [
    path("dj-admin/", admin.site.urls),

    path("blog/", include("apps.blog.urls")),          # CRUD
    path("", include("apps.blog.query_urls")),         # search/categories/tags/archives
    path("", include("apps.taxonomy.urls")),
    path("", include("apps.interactions.urls")),
    path("blog/search/", BlogSearchAPI.as_view()),     # README -> /blog/search/
    path("archives/", ArchiveMonthsAPI.as_view()),     # README -> /archives/
    path("archives/<int:year>/<int:month>/posts/", ArchivePostsAPI.as_view()),
]