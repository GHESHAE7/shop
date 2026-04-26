from django.db import models
from account_module.models import User
from product_module.models import ProductVariant
from product_module.models import Product
from django.utils.translation import gettext_lazy as _
from django.db.models import F, Sum



class Order(models.Model):
    class status_choices(models.TextChoices):
        CART = "cart", _("cart")
        PAID = "paid", _("paid")
        CANCELLED = "cancelled", _("cancelled")
        PROCESSING = "processing", _("processing")
        SHIPPED = "shipped", _("shipped")
        COMPLETED = "completed", _("completed")
        RETURNED = "returned", _("returned")
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=150, choices=status_choices, default=status_choices.CART)
    total_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    rahgiri_code = models.CharField(max_length=200, null=True, blank=True, verbose_name='کد رهگیری پرداخت سفارش')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس تحویل گیرنده')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_active = models.BooleanField(default=True, null=False, verbose_name='فعال / غیر فعال')
        
    def show_total_price(self):
        total = self.order_items.aggregate(total = Sum(F('price') * F('count')))['total'] or 0
        return total
    
    def __str__(self):
        return str(self.id)
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True, null=True)   
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_active = models.BooleanField(default=True, null=False, verbose_name='فعال / غیر فعال')
    
    def save(self, *args, **kwargs):
        self.product = self.product_variant.product
        if self.product_variant.discount:
            discount = self.product_variant.discount
            self.price = self.product.price - ((self.product.price / 100) * discount)
        else:
            self.price = self.product.price

        super(OrderItem, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.pk)
    