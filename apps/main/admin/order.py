from django.contrib import admin
from main.models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'client', 'deliver', 'cashier', 'total_price')
    list_display_links = ('id',)
    list_filter = ('status', 'deliver', 'cashier')
    search_fields = ['status', 'deliver', 'cashier']
    list_editable = ('status', 'client', 'deliver', 'cashier')


admin.site.register(Order, OrderAdmin)
