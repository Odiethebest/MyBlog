from django.contrib import admin
from django.urls import path, include
from apps.blog.views import BlogSearchAPI, ArchiveMonthsAPI, ArchivePostsAPI
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("dj-admin/", admin.site.urls),

    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # README required endpoints
    path("blog/search/", BlogSearchAPI.as_view(), name="blog-search"),
    path("archives/", ArchiveMonthsAPI.as_view(), name="archive-months"),
    path("archives/<int:year>/<int:month>/posts/", ArchivePostsAPI.as_view(), name="archive-posts"),

    #interactions 全部都挂在 /api/ 下
    path("api/", include("apps.interactions.urls")),

    # blog CRUD
    path("blog/", include("apps.blog.urls")),

    # other APIs
    path("", include("apps.blog.query_urls")),
    path("", include("apps.taxonomy.urls")),
]