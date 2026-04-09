from django.db import models

# Create your models here.


class About(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='نام درباره ما')
    description = models.TextField(null=False, blank=False, verbose_name='متن درباره ما')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_active = models.BooleanField(default=True, null=False, verbose_name='فعال / غیر فعال')
    
    
    def __str__(self):
        return self.name