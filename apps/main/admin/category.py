from django.contrib import admin
from main.models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_parent', 'parent',)
    list_display_links = ('name',)
    list_filter = ('is_parent', 'parent',)
    search_fields = ['is_parent', 'parent', ]
    list_editable = ('is_parent', 'parent',)


admin.site.register(Category, CategoryAdmin)
