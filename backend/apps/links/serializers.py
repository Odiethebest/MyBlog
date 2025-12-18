from rest_framework import serializers
from .models import FriendLink

class FriendLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendLink
        fields = "__all__"
        read_only_fields = ["id"]