# Django
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from finance.views import TransactionModelViewSet

router = DefaultRouter()
router.register(r'transaction', TransactionModelViewSet, 'transaction')

group_router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]
