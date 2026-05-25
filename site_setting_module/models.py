from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Baner(models.Model):
    title = models.CharField(max_length=60, null=False, blank=False, verbose_name="عنوان")
    description = models.CharField(max_length=100, null=True, blank=True, verbose_name="توضیحات")
    image = models.ImageField(max_length=500, null=False, blank=False, verbose_name="عکس", upload_to='baner/image')
    text_in_btn = models.CharField(max_length=100, null=False, blank=True, verbose_name='متن داخل دکمه')
    url_btn = models.URLField(max_length=600, null=False, blank=False, verbose_name='url دکمه')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_active = models.BooleanField(default=True, null=False, verbose_name='فعال / غیر فعال')
    
    def __str__(self):
        return self.title
    
    

class Elan(models.Model):
    
    class ChoicesWhere(models.TextChoices):
        top = 'top', _('top')
        buttom = 'buttom', _('buttom')

    title = models.CharField(max_length=300, null=False, blank=False, verbose_name='عنوان')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name="توضیحات")
    image = models.ImageField(max_length=500, null=True, blank=True, verbose_name="بکگراند", upload_to='elan/image')
    image_in_elan = models.ImageField(max_length=500, null=True, blank=True, verbose_name="عکس داخل متن", upload_to='baner/text/image')
    text_in_btn = models.CharField(max_length=200, null=False, blank=True, verbose_name='متن داخل دکمه')
    url_btn = models.URLField(max_length=600, null=False, blank=False, verbose_name='url دکمه')
    where = models.CharField(choices=ChoicesWhere, null=False, blank=False, max_length=10,)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_active = models.BooleanField(default=True, null=False, verbose_name='فعال / غیر فعال')
    
    
    def __str__(self):
        return f"{self.title} / {self.id}"
    
    

class SettingSite(models.Model):
    logo = models.ImageField(null=False, blank=False, upload_to='logo/image', verbose_name='لوگو سایت')
    name = models.CharField(null=False, blank=False, default='', verbose_name='نام سایت')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_active = models.BooleanField(default=True, null=False, verbose_name='فعال / غیر فعال')
    
    
    def __str__(self):
        return self.name