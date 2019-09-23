# Project
from django.db.models import OuterRef, Subquery, DecimalField
from django.db.models import Sum, F

from main.managers import BaseManager


class ProductBalanceManager(BaseManager):
    def products(self):
        from main.models import Product, Stock

        availability = F('total_balance') - F('total_defect')
        stocks = Stock.objects.all()
        product = Product.objects.all()
        output = DecimalField(max_digits=20, decimal_places=9)

        queryset = self.filter(stock=OuterRef("pk"), product=OuterRef('pk'))
        balance = queryset
        balance = balance.order_by()
        balance = balance.annotate(balance_total=Sum('balance'))
        balance = balance.values("balance_total")
        balance.query.group_by = []

        defect = queryset
        defect = defect.order_by()
        defect = defect.annotate(defect_total=Sum('defect'))
        defect = defect.values("defect_total")
        defect.query.group_by = []

        product = product.annotate(total_balance=Subquery(balance[:1], output_field=output))
        product = product.annotate(total_defect=Subquery(defect[:1], output_field=output))
        product = product.annotate(available=availability)
        product = product.values("id", "stock",  "product" "total_balance", "total_defect", 'available')


        return product
