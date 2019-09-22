from django.db import models

# Project
from main.models import (BaseMeta, BaseModel, DeleteMixin)
from main.managers import StockManager


class Stock(DeleteMixin, BaseModel):
    name = models.CharField(max_length=255)
    employees = models.ManyToManyField('main.User', through='main.Membership', related_name='stocks')
    address = models.CharField(max_length=255, null=True)
    objects = StockManager()

    def __str__(self):
        return self.name

    def get_members(self):
        return Membership.objects.filter(stock=self.id)

    class Meta(BaseMeta):
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'


class Membership(DeleteMixin, BaseModel):
    EMPLOYEE = 'employee'
    MANAGER = 'manager'
    OWNER = 'owner'

    POSITION_TYPES = (
        (EMPLOYEE, 'employee'),
        (MANAGER, 'manager'),
        (OWNER, 'owner'),
    )
    member = models.ForeignKey('main.User', on_delete=models.CASCADE, related_name='memberships')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='stocks')
    date_joined = models.DateField(null=True)
    role = models.CharField(max_length=10, choices=POSITION_TYPES, default=EMPLOYEE)

    def __str__(self):
        return self.role

    class Meta(BaseMeta):
        verbose_name = 'Membership'
        verbose_name_plural = 'Memberships'
