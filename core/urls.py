from django.urls import path, include

_patterns = [
    path('users/', include('apps.users.urls', namespace='users'))
]

urlpatterns = [
    path('api/', include(_patterns))
]
