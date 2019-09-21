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
