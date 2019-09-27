# Project
from django.db.models import OuterRef, Subquery, DecimalField
from django.db.models import Sum, F

from main.managers import BaseManager


class ProductBalanceManager(BaseManager):
    def products(self, stock=None, product=None):
        availability = (F('total_balance') - F('total_defect')) - F('total_sold')

        query = self
        if stock and product:
            query = self.filter(stock=stock, product=product)
        query = query.values('product_id', 'stock_id')
        query = query.annotate(total_defect=Sum('defect'))
        query = query.annotate(total_balance=Sum('balance'))
        query = query.annotate(total_sold=Sum('sold'))
        query = query.annotate(available=availability).order_by()
        return query
