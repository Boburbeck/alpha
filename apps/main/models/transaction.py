# Django
from django.db import models
from django.utils.translation import gettext as _
# Project
from main.models import BaseModel
from main.models import BaseMeta
from main.models import DeleteMixin
from main.managers import TransactionManager


class Transaction(BaseModel, DeleteMixin):
    INCOME = '1'
    SPENT = '2'

    TRANSACTION_TYPE = (
        (INCOME, _('Income')),
        (SPENT, _('Spending')),
    )

    income_amount = models.DecimalField(max_digits=20, decimal_places=9, default=0)
    spent_amount = models.DecimalField(max_digits=20, decimal_places=9, default=0)
    transaction_type = models.CharField(max_length=8, choices=TRANSACTION_TYPE, default=INCOME)
    client = models.ForeignKey('main.Client', on_delete=models.PROTECT, related_name='transactions', null=True)
    order = models.ForeignKey('main.Order', on_delete=models.PROTECT, related_name='transactions', null=True)
    stock = models.ForeignKey('main.Stock', on_delete=models.PROTECT, related_name='transactions', null=True)
    comment = models.TextField(null=True)

    created_by = models.ForeignKey('main.User', on_delete=models.PROTECT, related_name='created_transactions')
    updated_by = models.ForeignKey('main.User', on_delete=models.PROTECT, related_name='updated_transactions', null=True)
    objects = TransactionManager()

    class Meta(BaseMeta):
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
