# Django
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stock.views import StockModelViewSet

router = DefaultRouter()
router.register(r'stock', StockModelViewSet, 'stock')

group_router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]
