from django.db import models
# Project
from main.models import (BaseMeta, BaseModel, DeleteMixin)


class SoldCost(DeleteMixin, BaseModel):
    product = models.ForeignKey('main.Product', models.PROTECT, related_name='sold_costs')
    price = models.DecimalField(max_digits=20, decimal_places=9, null=True)
    internal_price = models.DecimalField(max_digits=20, decimal_places=9, null=True)
    is_active = models.BooleanField(default=True)
    creator = models.ForeignKey('main.User', models.CASCADE, null=True)

    def __str__(self):
        return str(self.product)

    class Meta(BaseMeta):
        verbose_name = 'SoldCost'
        verbose_name_plural = 'SoldCosts'
