# Generated by Django 2.2.5 on 2019-09-24 19:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'ordering': ('-id',),
                'permissions': (('can_see_user_list', 'Can see user list'),),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('is_parent', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='main.Category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('inn', models.CharField(max_length=255, null=True, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=255, null=True)),
                ('in_blacklist', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('date_joined', models.DateField(null=True)),
                ('role', models.CharField(choices=[('employee', 'employee'), ('manager', 'manager'), ('owner', 'owner')], default='employee', max_length=10)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Membership',
                'verbose_name_plural': 'Memberships',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('payment_type', models.CharField(choices=[('cash', 'In cash'), ('bank', 'Enumeration')], max_length=4)),
                ('status', models.CharField(choices=[('1', 'Ready'), ('2', 'Transferred to the delivery department'), ('3', 'Delivered'), ('4', 'Order cancelled')], default='1', max_length=1)),
                ('total_price', models.DecimalField(decimal_places=9, default=0, max_digits=20)),
                ('internal_total_price', models.DecimalField(decimal_places=9, default=0, max_digits=20)),
                ('total_balance', models.DecimalField(decimal_places=9, default=0, max_digits=20)),
                ('internal_total_balance', models.DecimalField(decimal_places=9, default=0, max_digits=20)),
                ('deliver', models.BooleanField(default=False)),
                ('delivery_date', models.DateField(null=True)),
                ('delivery_price', models.DecimalField(decimal_places=9, default=0, max_digits=20, null=True)),
                ('internal_delivery_price', models.DecimalField(decimal_places=9, default=0, max_digits=20, null=True)),
                ('delivered', models.BooleanField(default=False)),
                ('order_number', models.IntegerField(null=True, unique=True)),
                ('cashier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order', to='main.Client')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_orders', to=settings.AUTH_USER_MODEL)),
                ('delivery_man', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delivery_orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ('-id',),
                'permissions': [('can_set_delivery_man', 'Can set delivery man'), ('can_see_own_orders', 'Can see own orders'), ('can_see_all_orders', 'Can see all orders'), ('can_mark_delivery', 'Can mark delivery'), ('can_cancel_order', 'Can cancel order')],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('ball', models.DecimalField(blank=True, decimal_places=9, max_digits=20, null=True)),
                ('code', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('comment', models.TextField(blank=True)),
                ('priority', models.IntegerField(null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product', to='main.Category')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255, null=True)),
                ('employees', models.ManyToManyField(related_name='stocks', through='main.Membership', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Stock',
                'verbose_name_plural': 'Stocks',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='SoldCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=9, max_digits=20, null=True)),
                ('internal_price', models.DecimalField(decimal_places=9, max_digits=20, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sold_costs', to='main.Product')),
            ],
            options={
                'verbose_name': 'SoldCost',
                'verbose_name_plural': 'SoldCosts',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='ProductBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('balance', models.DecimalField(decimal_places=9, default=0, max_digits=20)),
                ('defect', models.DecimalField(decimal_places=9, default=0, max_digits=20)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_balances', to='main.Product')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_balances', to='main.Stock')),
            ],
            options={
                'verbose_name': 'Product Balance',
                'verbose_name_plural': 'Product Balances',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=9, max_digits=20)),
                ('price', models.DecimalField(decimal_places=9, max_digits=20)),
                ('internal_price', models.DecimalField(decimal_places=9, max_digits=20)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='main.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_products', to='main.Product')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_products', to='main.Stock')),
            ],
            options={
                'verbose_name': 'Order Product',
                'verbose_name_plural': 'Order Products',
                'ordering': ('-id',),
                'permissions': (('can_change_price', 'Can change price'),),
            },
        ),
        migrations.AddField(
            model_name='order',
            name='products_set',
            field=models.ManyToManyField(related_name='orders', through='main.OrderProduct', to='main.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='NetCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=9, max_digits=20, null=True)),
                ('internal_price', models.DecimalField(decimal_places=9, max_digits=20, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='net_costs', to='main.Product')),
            ],
            options={
                'verbose_name': 'NetCost',
                'verbose_name_plural': 'NetCosts',
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='membership',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='main.Stock'),
        ),
    ]
