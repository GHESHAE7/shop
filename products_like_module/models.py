from django.db import models
from account_module.models import User
from product_module.models import Product
# Create your models here.


class LikesProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name='کاربر')
    product = models.OneToOneField(Product, on_delete=models.CASCADE, null=False, blank=False, verbose_name='محصول', related_name='products_like')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_active = models.BooleanField(default=True, null=False, verbose_name='فعال / غیر فعال')
    
    def __str__(self):
        return self.user.username if self.user.username else self.user.email