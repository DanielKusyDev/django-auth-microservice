from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, AllowAny

from apps.users import serializers
from common.views import ModelViewSet, APIView

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    permission_required = {
        'update': 'is_account_owner',
        'partial_update': 'is_account_owner',
        'destroy': 'users.delete',
    }
    filterset_fields = ('is_staff',)


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
    queryset = User.objects.all()
    serializer_class = serializers.ChangePasswordSerializer
    http_method_names = ['put']
    permission_required = 'is_account_owner'

    def put(self, request, *args, pk=None, **kwargs):
        user = get_object_or_404(queryset=self.queryset, pk=pk)
        _serializer = self.serializer_class(data=request.data, instance=user)
        if _serializer.is_valid():
            _serializer.save()
            return self.success(status=200)
        return self.fail(status=400, errors=_serializer.errors)
