from django.db import models

# Project
from main.models import (BaseMeta, BaseModel, DeleteMixin)


class Client(DeleteMixin, BaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    inn = models.CharField(max_length=255, unique=True, null=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    in_blacklist = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta(BaseMeta):
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
