from django.db import models
from product_module.models import Product
from account_module.models import User

# Create your models here.


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False, verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name='کاربر')
    message = models.TextField(null=False, blank=False, verbose_name='متن کامنت')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_active = models.BooleanField(default=True, null=False, verbose_name='فعال / غیر فعال')
    
    def __str__(self):
        return self.product.name + '/' + self.user.email