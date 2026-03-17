from django.contrib import admin
from .models import Support, SupportCategory
# Register your models here.


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('name', 'is_active', 'updated_at', 'created_at',)
    list_filter = ('is_active', 'created_at',)
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at',)
    search_fields = ('category', 'name',)
    
    

@admin.register(SupportCategory)
class SupportCategoryAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('name', 'is_active', 'updated_at', 'created_at',)
    list_filter = ('is_active', 'created_at',)
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at',)
    search_fields = ('name',)