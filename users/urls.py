from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users import views


app_name = 'users'

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='regular')

urlpatterns = [
    path('', include(router.urls)),

    path('users/password/<int:pk>/', views.ChangePasswordAPIView.as_view(), name='password'),
    path('users/password/lost/', views.reset_password_confirm, name="reset-password-confirm"),
    path('users/password/token/', views.reset_password_request_token, name="reset-password-request"),
]
