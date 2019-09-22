from django.contrib.auth.models import Permission

from main.models import User


def init_set_permission(user_instance: User, permission_key):
    permission = Permission.objects.filter(name=permission_key)
    permission = permission.first() if permission else None
    user_instance.user_permissions.add(permission)


def init_create_membership(stock, user, role):
    from datetime import date
    from main.models import Membership
    today = date.today()
    Membership.objects.create(
        stock=stock,
        member=user,
        role=role,
        date_joined=today
    )
