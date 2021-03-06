# Django
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import UserAuthView
from main.views import UserViewSet
from main.views import NetCostModelViewSet
from main.views import SoldCostModelViewSet
from main.views import OrderModelViewSet
from main.views import ProductBalanceModelViewSet
from main.views import CategoryModelViewSet
from main.views import ProductModelViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, 'user')
router.register(r'net_cost', NetCostModelViewSet, 'net_cost')
router.register(r'sold_cost', SoldCostModelViewSet, 'sold_cost')
router.register(r'order', OrderModelViewSet, 'order')
router.register(r'category', CategoryModelViewSet, 'category')
router.register(r'product', ProductModelViewSet, 'product')
router.register(r'product_balance', ProductBalanceModelViewSet, 'product_balance')

group_router = DefaultRouter()

urlpatterns = [
    path('user/auth/', UserAuthView.as_view(), name='auth'),
    path('', include(router.urls)),
]
