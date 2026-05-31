from django.contrib import admin
from .models import LikesProduct
# Register your models here.


@admin.register(LikesProduct)
class LikesProductAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = (
        "user__email",
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
    search_fields = ("products",)
