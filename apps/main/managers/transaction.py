# Project
from django.db.models import OuterRef, Subquery, DecimalField
from django.db.models import Sum, F

from main.managers import BaseManager


class TransactionManager(BaseManager):
    def orders(self, stock=None, order=None):
        availability = F('total_income') - F('total_spending')

        query = self
        if stock and order:
            query = self.filter(stock=stock, order=order)
        query = query.values('order_id', 'stock_id')
        query = query.annotate(total_income=Sum('income_amount'))
        query = query.annotate(total_spending=Sum('spent_amount'))
        query = query.annotate(available=availability).order_by()
        return query
