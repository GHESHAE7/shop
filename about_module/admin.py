from django.contrib import admin
from .models import About
# Register your models here.


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'updated_at', 'created_at',)
    list_filter = ('created_at', 'updated_at', 'is_active', 'name')
    list_editable = ('is_active',)
    readonly_fields = ('updated_at', 'created_at',)