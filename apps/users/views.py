from django.contrib.auth import get_user_model

from apps.users import serializers
from common.views import ModelViewSet

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_required = {
        'update': 'is_account_owner',
        'partial_update': 'is_account_owner',
        'destroy': 'is_staff',
    }
