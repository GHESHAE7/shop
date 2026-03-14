from django.contrib import admin
from .models import Comment
# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product__name', 'user__email', 'is_active', 'updated_at', 'created_at',)
    list_filter = ('product', 'is_active', 'updated_at', 'created_at',)
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at',)
    date_hierarchy = 'created_at'
    search_fields = ('product', 'user', 'message')