from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users import views

app_name = 'users'

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('staff', views.StaffViewSet, basename='staff')

urlpatterns = [
    # ViewSets
    path('', include(router.urls)),

    # APIViews
    path('password/', views.ChangePasswordAPIView.as_view(), name='password_change')

]
