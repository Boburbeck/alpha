# Project
from django.db.models import OuterRef, Subquery, DecimalField
from django.db.models import Sum, Count

from main.managers import BaseManager


class StockManager(BaseManager):
    def employees(self):
        from main.models import Membership
        stock = self.all()
        output = DecimalField(max_digits=20, decimal_places=9)

        members = Membership.objects.filter(stock=OuterRef("id"))
        members = members.order_by()
        members = members.annotate(employee=Count('id'))
        members = members.values('employee')
        members.query.group_by = []

        stock = stock.annotate(staff=Subquery(members[:1], output_field=output))
        stock = stock.values('id', 'name', 'staff')
        return stock
