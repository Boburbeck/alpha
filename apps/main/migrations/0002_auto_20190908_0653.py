# Generated by Django 2.2.5 on 2019-09-08 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('-id',), 'permissions': (('can_see_user_list', 'Can see user list'),), 'verbose_name': 'User'},
        ),
    ]
