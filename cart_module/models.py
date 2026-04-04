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
    order_number = models.IntegerField()
    status = models.CharField(max_length=150, choices=status_choices)
    total_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_active = models.BooleanField(default=True, null=False, verbose_name='فعال / غیر فعال')

    
    def save(self, *args, **kwargs):
        last_order_number = Order.objects.filter(is_active=True).order_by('order_number').last()
        if last_order_number:
            self.order_number = last_order_number.order_number + 1
        else:
            self.order_number = 3355
        super(Order, self).save(*args, **kwargs)
        
    def show_total_price(self):
        total = self.order_items.aggregate(total = Sum(F('price') * F('count')))['total'] or 0
        return total
    
    def __str__(self):
        return str(self.order_number)
    
    
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
        p_v = ProductVariant.objects.filter(is_active=True, id=self.product_variant_id).first()
        self.price = p_v.price
        # self.product = self.product_variant__product
        super(OrderItem, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.pk)
    