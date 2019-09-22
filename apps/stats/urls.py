# Django
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stats.views import OrderStatsViewSet

router = DefaultRouter()
router.register(r'order', OrderStatsViewSet, 'order')

group_router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]
