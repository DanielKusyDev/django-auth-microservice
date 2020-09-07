from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAdminUser

from apps.users import serializers
from common.views import ModelViewSet

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.non_staff()
    serializer_class = serializers.UserSerializer
    permission_required = {
        'update': 'is_account_owner',
        'partial_update': 'is_account_owner',
        'destroy': 'users.delete',
    }


class StaffViewSet(ModelViewSet):
    queryset = User.objects.staff()
    serializer_class = serializers.StaffSerializer
    permission_required = {
        'update': 'is_account_owner',
        'partial_update': 'is_account_owner',
        'destroy': 'is_account_owner',
    }
    permission_classes = [IsAdminUser]
