from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import FriendLink
from .serializers import FriendLinkSerializer
from apps.interactions.pagination import StandardPagination  # 复用你现有分页（如果路径不同就改成你真实的）

class FriendLinkListAPI(generics.ListAPIView):
    serializer_class = FriendLinkSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardPagination

    def get_queryset(self):
        qs = FriendLink.objects.all()
        # 如果你模型里有 is_active 字段就打开下面两行；没有就删掉
        if hasattr(FriendLink, "is_active"):
            qs = qs.filter(is_active=True)
        # 如果你模型里有 sort_order 字段就按它排序；没有就默认 id
        if hasattr(FriendLink, "sort_order"):
            qs = qs.order_by("sort_order", "id")
        else:
            qs = qs.order_by("id")
        return qs

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        ser = self.get_serializer(page, many=True)
        p = self.paginator
        return Response({
            "page": p.page.number,
            "page_size": p.get_page_size(request),
            "total": qs.count(),
            "links": ser.data,
        })


class AdminFriendLinkCreateAPI(generics.CreateAPIView):
    serializer_class = FriendLinkSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = FriendLink.objects.all()


class AdminFriendLinkRUDAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FriendLinkSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = FriendLink.objects.all()
    lookup_url_kwarg = "link_id"