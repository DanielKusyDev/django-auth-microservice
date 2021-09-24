from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django_rest_passwordreset import views as password_reset_views
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.swagger_utils import users_id_schema
from apps.users import serializers
from apps.users.serializers import JwtTokenSerializer
from common.views import APIView, ModelViewSet

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.non_staff()
    permission_required = {
        "create": "allow_any",
        "update": "is_account_owner",
        "partial_update": "is_account_owner",
        "destroy": "users.delete",
    }
    filterset_fields = ("groups__name",)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class StaffViewSet(UserViewSet):
    queryset = User.objects.staff()
    permission_required = "is_staff"


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer

    @swagger_auto_schema(method="post", request_body=users_id_schema)
    @action(methods=["post"], detail=True)
    def users(self, request, *args, **kwargs):
        group = self.get_object()
        for pk in request.data:
            group.user_set.add(pk)
        return self.success(status=201)


class ChangePasswordAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = serializers.ChangePasswordSerializer
    http_method_names = ["put"]
    permission_required = "is_account_owner"

    def put(self, request, *args, pk=None, **kwargs):
        user = get_object_or_404(queryset=self.queryset, pk=pk)
        _serializer = self.serializer_class(data=request.data, instance=user)
        if _serializer.is_valid():
            _serializer.save()
            return self.success(status=200)
        return self.fail(status=400, errors=_serializer.errors)


class ResetPasswordApiView(APIView, password_reset_views.ResetPasswordConfirm):
    http_method_names = ["put"]

    def put(self, request, *args, **kwargs):
        response = self.post(request, *args, **kwargs)
        return response


class ResetPasswordTokenApiView(
    APIView, password_reset_views.ResetPasswordRequestToken
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redirect_url = ""

    def post(self, *args, **kwargs):
        self.redirect_url = self.request.data.get("redirect_url")
        return super().post(*args, **kwargs)


class JwtTokenView(TokenObtainPairView):
    serializer_class = JwtTokenSerializer


reset_password_request_token = ResetPasswordTokenApiView.as_view()
reset_password_confirm = ResetPasswordApiView.as_view()
