from django.urls import path
from .views import FriendLinkListAPI, AdminFriendLinkCreateAPI, AdminFriendLinkRUDAPI

urlpatterns = [
    path("links/", FriendLinkListAPI.as_view()),

    # admin
    path("api/admin/links/", AdminFriendLinkCreateAPI.as_view()),
    path("api/admin/links/<int:link_id>/", AdminFriendLinkRUDAPI.as_view()),
]