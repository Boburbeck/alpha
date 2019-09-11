from django.contrib import admin
from main.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'ball', 'code', 'creator',)
    list_display_links = ('name',)
    list_filter = ('category', 'ball', 'code', 'creator',)
    search_fields = ['category', 'ball', 'code', 'creator']
    list_editable = ('category', 'ball', 'code', 'creator')


admin.site.register(Product, ProductAdmin)
