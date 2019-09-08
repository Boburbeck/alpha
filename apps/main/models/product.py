from django.db import models
# Project
from main.models import (BaseMeta, BaseModel, DeleteMixin)


class Product(DeleteMixin, BaseModel):
    category = models.ForeignKey('main.Category', models.PROTECT, 'product', null=True)
    name = models.CharField(max_length=255)
    ball = models.DecimalField(max_digits=20, decimal_places=9, null=True, blank=True)
    code = models.CharField(max_length=255, unique=True, null=True, blank=True)
    comment = models.TextField(blank=True)

    priority = models.IntegerField(null=True)
    creator = models.ForeignKey('main.User', models.CASCADE, null=True)

    def __str__(self):
        return str(self.name)

    class Meta(BaseMeta):
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
