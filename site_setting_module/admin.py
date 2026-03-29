from django.contrib import admin
from .models import Baner

# Register your models here.


@admin.register(Baner)
class BanerAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('title', 'url_btn', 'is_active', 'updated_at', 'created_at',)
    list_filter = ('is_active', 'created_at', 'updated_at',)
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at',)
    search_fields = ('title', 'description', 'url_btn', 'text_in_btn')