from django.contrib import admin
from main.models import Stock


class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    list_display_links = ('name',)
    list_filter = ('name', 'address')
    search_fields = ['name', 'address']
    list_editable = ('address',)


admin.site.register(Stock, StockAdmin)
