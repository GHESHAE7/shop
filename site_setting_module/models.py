from django.db import models

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