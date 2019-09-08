from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from main.managers import UserManager

# Project
from main.models import (BaseMeta, BaseModel, DeleteMixin)


class User(AbstractBaseUser, PermissionsMixin, DeleteMixin, BaseModel):
    username = models.CharField(verbose_name=_('username'), unique=True, max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return str(self.username)

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def is_member(self, *groups):
        return self.groups.filter(name__in=groups).exists()

    def get_user_permissions(self):
        return Permission.objects.filter(
            Q(group__in=self.groups.all()) | Q(pk__in=self.user_permissions.all().values('id'))
        ).order_by('id').distinct('id')

    class Meta(BaseMeta):
        verbose_name = 'User'
        permissions = (
            ('can_see_user_list', 'Can see user list'),
        )
