from django.contrib import admin
from main.models import OrderProduct


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'amount', 'price',)
    list_display_links = ('id',)
    list_filter = ('order', 'product', 'amount', 'price',)
    search_fields = ['order', 'product', 'amount', 'price', ]
    list_editable = ('order', 'product', 'amount', 'price',)


admin.site.register(OrderProduct, OrderProductAdmin)
