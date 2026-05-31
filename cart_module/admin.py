from django.contrib import admin
from cart_module.models import Order, OrderItem, DiscountCode, UserDiscountUsage
# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "is_active",
        "total_price",
        "updated_at",
        "created_at",
    )
    list_filter = (
        "status",
        "is_active",
        "updated_at",
        "created_at",
    )
    search_fields = ("user", "status", "rahgiri_code")
    readonly_fields = (
        "created_at",
        "updated_at",
        "total_price",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product",
        "product_variant",
        "count",
        "is_active",
        "updated_at",
        "created_at",
    )
    list_filter = (
        "order",
        "product",
        "count",
        "product_variant",
        "is_active",
        "updated_at",
        "created_at",
    )
    search_fields = (
        "product__product_name",
        "order__id",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "price",
        "product",
    )


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "percent",
        "expires_at",
        "max_uses",
        "is_active",
        "updated_at",
        "created_at",
    )
    list_filter = (
        "percent",
        "expires_at",
        "max_uses",
        "is_active",
        "updated_at",
        "created_at",
    )
    list_editable = ("is_active",)
    search_fields = (
        "code",
        "percent",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(UserDiscountUsage)
class UserDiscountUsageAdmin(admin.ModelAdmin):
    list_display = (
        "user__username",
        "discount_code",
        "status_usage",
        "discount_amount_applied",
        "is_active",
        "updated_at",
        "created_at",
    )
    list_filter = (
        "user__username",
        "discount_code",
        "status_usage",
        "is_active",
        "updated_at",
        "created_at",
    )
    list_editable = ("is_active",)
    search_fields = ("user__username", "discount_code", "discount_amount_applied")
    readonly_fields = (
        "created_at",
        "updated_at",
        "discount_amount_applied",
    )
