from django.contrib import admin
from .models import Notice
# Register your models here.


# @admin.register(Notice)
# class NoticeAdmin(admin.ModelAdmin):
#     list_display = ('title', 'icon', 'is_active', 'updated_at', 'created_at',)
#     list_filter = ('created_at', 'updated_at', 'is_active', 'icon')
#     list_editable = ('is_active', 'icon')
#     readonly_fields = ('updated_at', 'created_at',)