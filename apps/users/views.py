from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser

from apps.users import serializers
from common.views import ModelViewSet, APIView

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


class ChangePasswordAPIView(APIView):
    def put(self, request, *args, **kwargs):
        _serializer = serializers.ChangePasswordSerializer(data=request.data, instance=request.user)
        if _serializer.is_valid():
            _serializer.save()
            return self.success(status=200)
        return self.fail(status=400, errors=_serializer.errors)
