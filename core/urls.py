from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    info=openapi.Info(
        title="Dan CRM API",
        default_version='v1',
        description="API for Dan CRM project.",
        contact=openapi.Contact(email="daniel.kusy97@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


_patterns = [
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='docs'),
    path('users/', include('apps.users.urls', namespace='users'))
]

urlpatterns = [
    path('api/', include(_patterns))
]
