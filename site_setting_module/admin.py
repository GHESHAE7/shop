from django.contrib import admin
from .models import Baner, Elan, SettingSite

# Register your models here.


@admin.register(Baner)
class BanerAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = (
        "title",
        "url_btn",
        "is_active",
        "updated_at",
        "created_at",
    )
    list_filter = (
        "is_active",
        "created_at",
        "updated_at",
    )
    list_editable = ("is_active",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "description", "url_btn", "text_in_btn")


@admin.register(Elan)
class ElanAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = (
        "title",
        "where",
        "url_btn",
        "is_active",
        "updated_at",
        "created_at",
    )
    list_filter = ("is_active", "created_at", "updated_at", "where")
    list_editable = ("is_active", "where")
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "description", "url_btn", "text_in_btn", "where")


@admin.register(SettingSite)
class ElanAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = (
        "name",
        "is_active",
        "updated_at",
        "created_at",
    )
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    readonly_fields = (
        "updated_at",
        "created_at",
    )
