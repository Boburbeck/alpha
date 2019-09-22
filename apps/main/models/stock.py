from django.db import models

# Project
from main.models import (BaseMeta, BaseModel, DeleteMixin)


class Stock(DeleteMixin, BaseModel):
    name = models.CharField(max_length=255)
    employees = models.ManyToManyField('main.User', related_name='stocks')
    address = models.CharField(max_length=255, null=True)
    created_by = models.ForeignKey('main.User', on_delete=models.PROTECT, related_name='stock')

    def __str__(self):
        return self.name

    class Meta(BaseMeta):
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
        permissions = (
            ('stock_owner', 'Stock owner'),
            ('stock_manager', 'Stock manager'),
        )


class Membership(DeleteMixin, BaseModel):
    EMPLOYEE = 'employee'
    MANAGER = 'manager'
    OWNER = 'owner'

    POSITION_TYPES = (
        (EMPLOYEE, 'employee'),
        (MANAGER, 'manager'),
        (OWNER, 'owner'),
    )
    employee = models.ForeignKey('main.User', on_delete=models.CASCADE, related_name='memberships')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='memberships')
    date_joined = models.DateField(null=True)
    role = models.CharField(max_length=10, choices=POSITION_TYPES, default=EMPLOYEE)
    created_by = models.ForeignKey('main.User', on_delete=models.PROTECT, related_name='memberships')

    def __str__(self):
        return self.role

    class Meta(BaseMeta):
        verbose_name = 'Membership'
        verbose_name_plural = 'Memberships'
        permissions = (
            ('stock_owner', 'Stock owner'),
            ('stock_manager', 'Stock manager'),
        )