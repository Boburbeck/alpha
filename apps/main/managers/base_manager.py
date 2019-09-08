from django.db import models


class QuerySet(models.QuerySet):
    def delete(self):
        self.update(is_delete=True)


class BaseManager(models.Manager):
    def get_queryset(self):
        return QuerySet(self.model).filter(is_delete=False)
