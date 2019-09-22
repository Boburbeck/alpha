# Django
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stock.views import StockModelViewSet
from stock.views import MembershipModelViewSet

router = DefaultRouter()
router.register(r'stock', StockModelViewSet, 'stock')
router.register(r'staff', MembershipModelViewSet, 'staff')

group_router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]
