# Django
from django.db import models
from django.utils.translation import gettext as _
# Project
from main.models import BaseModel
from main.models import BaseMeta
from main.models import DeleteMixin


class Order(BaseModel, DeleteMixin):
    READY = '1'
    GIVEN = '2'
    DELIVERED = '3'
    CANCELLED = '4'

    ORDER_STATUS = (
        (READY, _('Ready')),
        (GIVEN, _('Transferred to the delivery department')),
        (DELIVERED, _('Delivered')),
        (CANCELLED, _('Order cancelled')),
    )

    CASH = 'cash'
    BANK = 'bank'
    PAYMENT_TYPE = (
        (CASH, _('In cash')),
        (BANK, _("Enumeration")),
    )

    cashier = models.ForeignKey('main.User', on_delete=models.CASCADE, related_name='orders')
    payment_type = models.CharField(max_length=4, choices=PAYMENT_TYPE)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default=READY)
    client = models.ForeignKey('main.Client', on_delete=models.PROTECT, related_name='order')
    products_set = models.ManyToManyField('main.Product', through='main.OrderProduct', related_name='orders')

    total_price = models.DecimalField(max_digits=20, decimal_places=9, default=0)
    internal_total_price = models.DecimalField(max_digits=20, decimal_places=9, default=0)

    total_balance = models.DecimalField(max_digits=20, decimal_places=9, default=0)
    internal_total_balance = models.DecimalField(max_digits=20, decimal_places=9, default=0)

    deliver = models.BooleanField(default=False)
    delivery_man = models.ForeignKey('main.User', on_delete=models.CASCADE, related_name='delivery_orders', null=True)
    delivery_date = models.DateField(null=True)
    delivery_price = models.DecimalField(max_digits=20, decimal_places=9, null=True, default=0)
    internal_delivery_price = models.DecimalField(max_digits=20, decimal_places=9, null=True, default=0)
    delivered = models.BooleanField(default=False)

    created_by = models.ForeignKey('main.User', on_delete=models.PROTECT, related_name='created_orders')
    updated_by = models.ForeignKey('main.User', on_delete=models.PROTECT, related_name='updated_orders', null=True)
    order_number = models.IntegerField(unique=True, null=True)

    class Meta(BaseMeta):
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        permissions = [
            ('can_set_delivery_man', 'Can set delivery man'),
            ('can_see_own_orders', 'Can see own orders'),
            ('can_see_all_orders', 'Can see all orders'),
            ('can_mark_delivery', "Can mark delivery"),
            ('can_cancel_order', 'Can cancel order'),
        ]

    def __str__(self):
        return str(self.id)

    def total_paid(self):
        return self.total_price - self.total_balance


class OrderProduct(BaseModel, DeleteMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey('main.Product', on_delete=models.PROTECT, related_name='order_products')
    amount = models.DecimalField(max_digits=20, decimal_places=9)

    price = models.DecimalField(max_digits=20, decimal_places=9)
    internal_price = models.DecimalField(max_digits=20, decimal_places=9)

    class Meta(BaseMeta):
        verbose_name = 'Order Product'
        verbose_name_plural = 'Order Products'
        permissions = (
            ('can_change_price', 'Can change price'),
        )
