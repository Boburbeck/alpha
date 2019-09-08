# Django
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import UserAuthView
from main.views import UserViewSet
from main.views import NetCostModelViewSet
from main.views import SoldCostModelViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, 'user')
router.register(r'net_cost', NetCostModelViewSet, 'net_cost')
router.register(r'sold_cost', SoldCostModelViewSet, 'sold_cost')

group_router = DefaultRouter()

urlpatterns = [
    path('user/auth/', UserAuthView.as_view(), name='auth'),
    path('', include(router.urls)),
]
