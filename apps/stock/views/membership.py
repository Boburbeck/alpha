from rest_framework import viewsets

from main.models import Membership
from stock.serializers import MembershipModelSerializer

from main.filters import MembershipFilterSet


class MembershipModelViewSet(viewsets.ModelViewSet):
    """
    TEST
    """

    serializer_class = MembershipModelSerializer
    model = Membership
    queryset = Membership.objects.all()
    filter_class = MembershipFilterSet
