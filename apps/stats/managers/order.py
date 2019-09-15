# Project
from django.db.models import OuterRef, Subquery, DecimalField
from django.db.models import Sum

from main.managers import BaseManager


class OrderManager(BaseManager):
    def by_order(self):
        from main.models import Order
        from main.models import OrderProduct
        order = Order.objects.all()
        output = DecimalField(max_digits=20, decimal_places=9)
        order_product = OrderProduct.objects.filter(order=OuterRef("id"))
        order_product = order_product.order_by()
        order_product = order_product.annotate(total=Sum('price'))
        order_product = order_product.values('total')
        order_product.query.group_by = []

        order = order.annotate(children_total=Subquery(order_product[:1], output_field=output))
        order = order.values('id', 'children_total', 'internal_total_price', 'internal_total_balance',
                             'internal_delivery_price')
        return order


