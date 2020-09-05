from django.contrib.auth import get_user_model

from apps.users import serializers
from common.views import ModelViewSet

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.non_staff()
    serializer_class = serializers.UserSerializer

    permission_required = 'is_staff'
