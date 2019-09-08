# coding=utf-8
from typing import List

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

# Project
from main.managers import BaseManager


class UserManager(BaseUserManager, BaseManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given username, date of
        birth and password.
        """
        if not username:
            raise ValueError(_('Users must have an username address'))

        user = self.model(username=username.strip(), )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given username, date of
        birth and password.
        """
        user = self.create_user(username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user
