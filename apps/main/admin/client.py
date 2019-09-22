from django.contrib import admin
from main.models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'inn', 'phone_number', 'in_blacklist')
    list_display_links = ('first_name',)
    list_filter = ('last_name', 'inn', 'phone_number', 'in_blacklist')
    search_fields = ['last_name', 'inn', 'phone_number', 'in_blacklist']
    list_editable = ('last_name', 'inn', 'phone_number', 'in_blacklist')


admin.site.register(Client, ClientAdmin)
