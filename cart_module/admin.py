from django.contrib import admin
from cart_module.models import Order, OrderItem
# Register your models here.



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number','user', 'status', 'is_active', 'total_price', 'updated_at', 'created_at',)
    list_filter = ('order_number', 'status', 'is_active', 'updated_at', 'created_at',)
    search_fields = ('user','order_number', 'status', 'rahgiri_code')
    readonly_fields = ('created_at', 'updated_at', 'total_price', 'order_number',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'product_variant', 'count', 'is_active', 'updated_at', 'created_at',)
    list_filter = ('order', 'product', 'count', 'product_variant', 'is_active', 'updated_at', 'created_at',)
    search_fields = ('product__product_name', 'order__order_number',)
    readonly_fields = ('created_at', 'updated_at', 'price', 'product',)
