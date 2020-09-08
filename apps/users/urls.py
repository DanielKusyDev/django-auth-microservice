from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users import views

app_name = 'users'

router = DefaultRouter()
router.register('regular', views.UserViewSet, basename='regular')
router.register('staff', views.StaffViewSet, basename='staff')
router.register('password', views.PasswordViewSet, basename='password')

urlpatterns = [
    # ViewSets
    path('', include(router.urls)),
]
