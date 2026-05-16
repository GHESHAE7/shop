from django.db import models
from account_module.models import User
from product_module.models import ProductVariant
from product_module.models import Product
from django.utils.translation import gettext_lazy as _
from django.db.models import F, Sum
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator




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
        current_user_discount_usage = UserDiscountUsage.objects.filter(order_id=self.id, status_usage='not_used', is_active=True).first()
        if current_user_discount_usage:
            current_discount_code = DiscountCode.objects.filter(code=current_user_discount_usage.discount_code).first()
            total -= (total / 100) * current_discount_code.percent
            return total
        else:
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
    
    

class DiscountCode(models.Model):
    code = models.CharField(max_length=15, unique=True, verbose_name="کد تخفیف")
    percent = models.PositiveIntegerField(null=True, blank=True, verbose_name="درصد تخفیف", validators=[MinValueValidator(1), MaxValueValidator(100)])
    expires_at = models.DateTimeField(null=True,blank=True,verbose_name="تاریخ انقضا")
    max_uses = models.PositiveIntegerField(null=True, blank=True, verbose_name="حداکثر تعداد کل استفاده")
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_active = models.BooleanField(default=True, null=False, verbose_name='فعال / غیر فعال')
    
    def __str__(self):
        return self.code

    # def is_expired(self):
    #     if self.expires_at:
    #         self.is_active = False if timezone.now() > self.expires_at else True
            
    # def save(self, *args, **kwargs):
    #     if self.id:
    #         self.is_active = False if timezone.now() > self.expires_at else True
    #     super(DiscountCode, self).save(*args, **kwargs)
            
            

class UserDiscountUsage(models.Model):
    class status_choices(models.TextChoices):
        NOT_USED = "not_used", _("not_used")
        USED = "used", _("used")
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="discount_usages", verbose_name="کاربر")
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE, related_name="usages", verbose_name="کد تخفیف")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name="discounts_applied", verbose_name="سفارش مربوط")
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_active = models.BooleanField(default=True, null=False, verbose_name='فعال / غیر فعال')
    status_usage = models.CharField(max_length=150, choices=status_choices, default=status_choices.NOT_USED)
    discount_amount_applied = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="مبلغ تخفیف اعمال شده")


    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ['user', 'discount_code']