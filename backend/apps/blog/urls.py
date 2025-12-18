from django.urls import path
from .views import BlogListCreateView, BlogRetrieveUpdateDeleteView

urlpatterns = [
    path("", BlogListCreateView.as_view(), name="blog-list-create"),
    path("<int:post_id>/", BlogRetrieveUpdateDeleteView.as_view(), name="blog-rud"),
]