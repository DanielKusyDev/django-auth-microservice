from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import JwtTokenView
from core.settings import BASE_API_URL

schema_view = get_schema_view(
    info=openapi.Info(
        title="Django authorization API",
        default_version="v1",
        contact=openapi.Contact(email="daniel.kusy97@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="docs"),
    path(f"{BASE_API_URL}token/", JwtTokenView.as_view(), name="token_obtain_pair"),
    path(
        f"{BASE_API_URL}token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(f"{BASE_API_URL}", include("apps.users.urls", namespace="users")),
]
