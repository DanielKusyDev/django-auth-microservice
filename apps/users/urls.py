from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users import views

app_name = 'users'

router = DefaultRouter()
router.register('regular', views.UserViewSet, basename='regular')
router.register('staff', views.StaffViewSet, basename='staff')

urlpatterns = [
    path('', include(router.urls)),

    path('password/<int:pk>/', views.ChangePasswordAPIView.as_view(), name='password'),
    path('password/lost/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
