from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from django_rest_passwordreset.views import ResetPasswordRequestToken, ResetPasswordConfirm, ResetPasswordValidateToken
from rest_framework.permissions import AllowAny

from apps.users import serializers
from common.views import ModelViewSet, APIView

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    permission_required = {
        'update': 'is_account_owner',
        'partial_update': 'is_account_owner',
        'destroy': 'users.delete',
    }
    filterset_fields = ('is_staff',)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


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


class ResetPasswordConfirmationApiView(ResetPasswordConfirm):
    permission_classes = [AllowAny]


class ResetPasswordTokenValidationApiView(ResetPasswordValidateToken):
    permission_classes = [AllowAny]


class ResetPasswordTokenRequestApiView(ResetPasswordRequestToken):
    permission_classes = [AllowAny]


reset_password_validate_token = ResetPasswordTokenValidationApiView.as_view()
reset_password_confirm = ResetPasswordConfirmationApiView.as_view()
reset_password_request_token = ResetPasswordTokenRequestApiView.as_view()
