# Django
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import UserAuthView
from main.views import LogOutView
from main.views import UserViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, 'user')

group_router = DefaultRouter()

urlpatterns = [
    path('user/auth/', UserAuthView.as_view(), name='auth'),
    path('', include(router.urls)),
]
