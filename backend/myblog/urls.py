from django.contrib import admin
from django.urls import path, include
from apps.blog.views import BlogSearchAPI, ArchiveMonthsAPI, ArchivePostsAPI
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("dj-admin/", admin.site.urls),

    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("blog/", include("apps.blog.urls")),
    path("", include("apps.blog.query_urls")),
    path("", include("apps.taxonomy.urls")),
    path("api/", include("apps.interactions.urls")),
    path("blog/search/", BlogSearchAPI.as_view()),
    path("archives/", ArchiveMonthsAPI.as_view()),
    path("archives/<int:year>/<int:month>/posts/", ArchivePostsAPI.as_view()),
]