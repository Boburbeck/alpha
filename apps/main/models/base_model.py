from django.db import models

from main.managers import BaseManager


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DeleteMixin(models.Model):
    is_delete = models.BooleanField(default=False)

    objects = BaseManager()

    class Meta:
        abstract = True


class BaseMeta(object):
    ordering = ('-id',)
    # default_permissions = DEFAULT_PERMISSIONS
