# Generated by Django 2.2.5 on 2019-09-25 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_productbalance_sold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('1', 'Ready'), ('2', 'Transferred to the delivery department'), ('3', 'Delivered'), ('4', 'Done'), ('5', 'Order cancelled')], default='1', max_length=1),
        ),
    ]