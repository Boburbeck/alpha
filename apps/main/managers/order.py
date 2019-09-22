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

    def by_cashier(self, cashier=None):
        from main.models import Order, OrderProduct, User

        if cashier:
            user = User.objects.filter(username=cashier)
        else:
            user = User.objects.all()
        # user.filter(username=cashier) if cashier else user
        output = DecimalField(max_digits=20, decimal_places=9)
        order = Order.objects.filter(cashier=OuterRef("pk"))
        order = order.order_by()
        order = order.annotate(total_sale=Sum('internal_total_price'))
        order = order.values('total_sale')
        order.query.group_by = []

        user = user.annotate(sales=Subquery(order[:1], output_field=output))
        user = user.values('id', 'first_name', 'last_name', 'sales')
        user = user.exclude(sales__isnull=True)
        return user
