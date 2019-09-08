from django.db import models

# Project
from main.models import (BaseMeta, BaseModel, DeleteMixin)


class Category(DeleteMixin, BaseModel):
    name = models.CharField(max_length=255)
    is_parent = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='children')

    def __str__(self):
        return str(self.name)

    class Meta(BaseMeta):
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
