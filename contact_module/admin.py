from django.contrib import admin
from .models import ContactUs
# Register your models here.


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('name', 'email', 'subject', 'is_read_by_admin', 'is_active', 'updated_at', 'created_at',)
    list_filter = ('subject', 'is_read_by_admin', 'is_active', 'created_at',)
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at',)
    search_fields = ('subject', 'email', 'name',)