from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users import views

app_name = 'users'

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='regular')

urlpatterns = [
    path('', include(router.urls)),

    path('users/password/<int:pk>/', views.ChangePasswordAPIView.as_view(), name='password'),
    path('users/password/lost/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
